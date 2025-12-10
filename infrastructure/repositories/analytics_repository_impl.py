import logging
import pandas as pd
import numpy as np
import xgboost as xgb
import pathlib
from typing import Tuple, Dict, Any, Optional
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score

from domain.entities.analytics import StudentFeatures, RiskPrediction, TrainingStatus
from domain.repositories.analytics_repository import AnalyticsRepository

# Configuración de Logging
logger = logging.getLogger(__name__)

# Rutas configurables
BASE_DIR = pathlib.Path("data")
MODEL_PATH = pathlib.Path("models/dropout_xgb.json")
DATA_PATH_VIVIENDA = BASE_DIR / "TVIVIENDA.csv"
DATA_PATH_MODULO = BASE_DIR / "TMODULO.csv"

class XGBoostRepositoryImpl(AnalyticsRepository):
    def __init__(self):
        self.model: Optional[xgb.XGBClassifier] = None
        self._ensure_dirs()

    def _ensure_dirs(self):
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        BASE_DIR.mkdir(parents=True, exist_ok=True)

    def _load_model(self):
        if not self.model:
            if not MODEL_PATH.exists():
                raise FileNotFoundError(f"El modelo no existe en {MODEL_PATH}. Ejecute el entrenamiento primero.")
            self.model = xgb.XGBClassifier()
            self.model.load_model(str(MODEL_PATH))

    # --- ETL / Cleaning Helpers ---

    def _limpiar_target(self, val: Any) -> int:
        s = str(val).strip().split('.')[0]
        if s in ['2', '02']: return 1
        return 0

    def _limpiar_binario_feature(self, val: Any) -> int:
        s = str(val).strip().split('.')[0]
        if s in ['1', '01']: return 1
        return 0

    def _limpiar_horas(self, val: Any) -> float:
        try:
            v = str(val).strip()
            if v in ['99', 'b', 'nan']: return 0.0
            return float(v)
        except:
            return 0.0

    def _limpiar_recurso(self, val: Any) -> int:
        s = str(val).strip().split('.')[0]
        if s == '1': return 1
        return 0

    def _limpiar_trabajo(self, val: Any) -> int:
        try:
            v = int(val)
            return 1 if 1 <= v <= 6 else 0
        except:
            return 0

    def _limpiar_sexo(self, val: Any) -> int:
         return 1 if str(val).strip() in ['2', '02', '2.0'] else 0

    def _limpiar_escuela_publica(self, val: Any) -> int:
        return 1 if str(val).strip().split('.')[0] == '1' else 0

    def _preprocess_data(self, df_modulo: pd.DataFrame, df_vivienda: pd.DataFrame) -> pd.DataFrame:
        """
        Realiza el merge y la limpieza de datos para generar el dataset de entrenamiento.
        """
        # Limpieza de llaves para merge
        df_modulo['FOLIO'] = df_modulo['FOLIO'].astype(str).str.strip()
        df_vivienda['FOLIO'] = df_vivienda['FOLIO'].astype(str).str.strip()

        # Merge
        df_completo = pd.merge(df_modulo, df_vivienda, on='FOLIO', how='left')
        logging.info(f"Tablas unidas. Dimensiones: {df_completo.shape}")

        df_model = pd.DataFrame()

        # Target (PB3_1)
        df_model['Target'] = df_completo['PB3_1'].apply(self._limpiar_target).astype(int)

        # Features Mapping
        # P1_4_6 -> Internet_Casa
        df_model['Internet_Casa'] = df_completo['P1_4_6'].apply(self._limpiar_binario_feature)
        
        # P1_4_2 -> Tiene_Laptop
        df_model['Tiene_Laptop'] = df_completo['P1_4_2'].apply(self._limpiar_binario_feature)
        
        # SEXO -> Sexo_Femenino
        df_model['Sexo_Femenino'] = df_completo['SEXO'].apply(self._limpiar_sexo)
        
        # EDAD -> Edad
        df_model['Edad'] = pd.to_numeric(df_completo['EDAD'], errors='coerce').fillna(0)
        
        # PD3_1 -> Trabaja
        df_model['Trabaja'] = df_completo['PD3_1'].apply(self._limpiar_trabajo)
        
        # P1_1 -> Num_Personas_Casa
        df_model['Num_Personas_Casa'] = pd.to_numeric(df_completo['P1_1'], errors='coerce').fillna(1)
        
        # PA3_2 -> Escuela_Publica_Ant
        df_model['Escuela_Publica_Ant'] = df_completo['PA3_2'].apply(self._limpiar_escuela_publica)
        
        # PA3_4 -> Concluyo_Anterior
        df_model['Concluyo_Anterior'] = df_completo['PA3_4'].apply(self._limpiar_binario_feature)
        
        # PA3_7_3 -> Recurso_Materias
        df_model['Recurso_Materias'] = df_completo['PA3_7_3'].apply(self._limpiar_recurso)
        
        # PD3_2 -> Horas_Trabajo
        df_model['Horas_Trabajo'] = df_completo['PD3_2'].apply(self._limpiar_horas)

        return df_model

    # --- Public Methods ---

    def predict(self, student: StudentFeatures) -> RiskPrediction:
        try:
            self._load_model()
            
            # Mapeo de StudentFeatures al DataFrame esperado por el modelo
            # IMPORTANTE: El orden de columnas debe coincidir con el entrenamiento (XGBoost es sensible a esto, 
            # aunque usando un dict -> DataFrame con nombres de columnas debería manejarlo bien si se alinean).
            # Para mayor seguridad, definimos explícitamente el diccionario con las claves correctas.
            
            data = {
                'Internet_Casa': [student.internet_home],
                'Tiene_Laptop': [student.has_laptop],
                'Sexo_Femenino': [student.is_female],
                'Edad': [student.age],
                'Trabaja': [student.works],
                'Num_Personas_Casa': [student.num_people_home],
                'Escuela_Publica_Ant': [student.prev_school_public],
                'Concluyo_Anterior': [student.finished_prev_school],
                'Recurso_Materias': [student.repeated_subjects],
                'Horas_Trabajo': [student.work_hours]
            }
            
            input_df = pd.DataFrame(data)

            # Predecir
            probs = self.model.predict_proba(input_df)
            prob_dropout = float(probs[0][1]) # Probabilidad de clase 1 (Deserción)

            # Lógica de negocio para niveles de riesgo
            if prob_dropout > 0.7:
                level = "Alto"
                rec = "Intervención inmediata requerida. Contactar a tutoría."
            elif prob_dropout > 0.3:
                level = "Medio"
                rec = "Seguimiento académico semanal sugierido."
            else:
                level = "Bajo"
                rec = "Mantener monitoreo regular."

            return RiskPrediction(
                probability=prob_dropout,
                risk_level=level,
                recommendation=rec
            )
            
        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            # En caso de error crítico, podríamos propagar o retornar un default seguro.
            # Aquí propagamos para que el Use Case maneje el error.
            raise e

    def train_model(self) -> TrainingStatus:
        try:
            logger.info("Iniciando ciclo de entrenamiento...")
            
            if not DATA_PATH_MODULO.exists() or not DATA_PATH_VIVIENDA.exists():
                msg = f"Archivos CSV no encontrados en: {BASE_DIR}. Asegúrese de tener TMODULO.csv y TVIVIENDA.csv"
                logger.error(msg)
                return TrainingStatus(success=False, message=msg, accuracy=0.0)

            # 1. Cargar Datos
            logger.info("Cargando archivos CSV...")
            df_modulo = pd.read_csv(DATA_PATH_MODULO, encoding='latin-1', low_memory=False)
            df_vivienda = pd.read_csv(DATA_PATH_VIVIENDA, encoding='latin-1', low_memory=False)
            
            # 2. Preprocesar
            df_model = self._preprocess_data(df_modulo, df_vivienda)
            
            # Validar clases
            conteo = df_model['Target'].value_counts()
            if len(conteo) < 2:
                msg = "Error crítico: Solo se detectó una clase en el Target. No se puede entrenar."
                logger.error(msg)
                return TrainingStatus(success=False, message=msg, accuracy=0.0)

            X = df_model.drop('Target', axis=1)
            y = df_model['Target']

            # 3. Split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # 4. Calcular ratio para balanceo
            num_zeros = np.sum(y_train == 0)
            num_ones = np.sum(y_train == 1)
            if num_ones == 0:
                 scale_pos_weight = 1.0 # Evitar división por cero
            else:
                 scale_pos_weight = float(num_zeros) / float(num_ones)

            logger.info(f"Entrenando XGBoost con scale_pos_weight={scale_pos_weight:.2f}")

            # 5. Configurar y Entrenar Modelo
            model = xgb.XGBClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                objective='binary:logistic',
                base_score=0.5,
                scale_pos_weight=scale_pos_weight,
                random_state=42
            )
            
            model.fit(X_train, y_train)

            # 6. Evaluación
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            
            logger.info(f"Entrenamiento completado. Accuracy: {acc:.2%}")
            
            # 7. Guardar Modelo
            model.save_model(str(MODEL_PATH))
            self.model = model # Actualizar instancia en memoria

            return TrainingStatus(
                success=True,
                message=f"Modelo entrenado exitosamente. Precisión: {prec:.2f}, Recall: {rec:.2f}",
                accuracy=float(acc)
            )

        except Exception as e:
            logger.exception("Error durante el entrenamiento")
            return TrainingStatus(success=False, message=str(e), accuracy=0.0)