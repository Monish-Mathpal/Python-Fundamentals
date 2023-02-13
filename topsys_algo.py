from typing import Tuple, List
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from config.config import Config
config = Config()
app_config = config.read_config()

W1_course_duration =  0.25
W2_course_volume = 0.25
W3_course_cost = 0.25
# W4_course_total_disbursed_amount = 0.2
W5_course_dpd_days = 0.25

class Data:
    @staticmethod
    def get_connector():
        try:
            engine = create_engine(app_config.DSN)
            connection = engine.connect()
            return connection
        except Exception:
            raise ('connection error')

    @staticmethod
    def get_data(data_source, cols, conn):
        with conn as conn:
            data = pd.read_sql(f'select {cols} from {data_source}', conn)
        return data


def X_matrix(df: pd.DataFrame) -> np.array:
    return df.to_numpy()

def X_square(X: np.array) -> np.array:
    return X.T**2

def X_normalize(X: np.array, X_sqr: np.array) -> np.array:
    return X/np.sqrt(np.sum(X_sqr, axis=1))

def calculate_normalized_weighted_matrix(df: pd.DataFrame) -> np.array:
    X = X_matrix(df)
    X_sqr = X_square(X)
    X_normz = X_normalize(X, X_sqr)
    X_normz_w = np.prod([X_normz, np.array([[W1_course_duration], [W2_course_volume], [W3_course_cost],\
        [W5_course_dpd_days]]).T], axis=0)
    
    return X_normz_w

def get_optimize_rule(X):
    Si_plus_rule = np.max(X, axis=0)[0], np.min(X, axis=0)[1], np.max(X, axis=0)[2], np.min(X, axis=0)[3]
    # , np.max(X, axis=0)[4] 
    Si_minus_rule = np.min(X, axis=0)[0], np.max(X, axis=0)[1], np.min(X, axis=0)[2], np.max(X, axis=0)[3]
    # , np.min(X, axis=0)[4]
    
    return Si_plus_rule, Si_minus_rule

def calculate_si_plus_minus(df: pd.DataFrame) -> Tuple:
    X = calculate_normalized_weighted_matrix(df)
    Si_plus, Si_minus = get_optimize_rule(X)  
    
    return X, Si_plus, Si_minus

def calculate_pi_plus_minus(df: pd.DataFrame) -> Tuple[np.array]:
    X_Si_plus_Si_minus = calculate_si_plus_minus(df)
    Pi_plus = np.sqrt(np.sum((X_Si_plus_Si_minus[0]-X_Si_plus_Si_minus[1])**2, axis=1))
    Pi_minus = np.sqrt(np.sum((X_Si_plus_Si_minus[0]-X_Si_plus_Si_minus[2])**2, axis=1))
    return Pi_plus, Pi_minus
    
    
def rank_course(df: pd.DataFrame) -> List:
    Pi_plus_minus = calculate_pi_plus_minus(df) 
    
    return [round(val,3)  for val in np.round(Pi_plus_minus[1]/(Pi_plus_minus[0] + Pi_plus_minus[1]),2)*100]
