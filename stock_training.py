from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
import pandas as pd

def get_stock_training(stock,cleaned_file):
    cleaned_file="".join(cleaned_file)
    df=pd.read_csv(cleaned_file)
    print(df.head())
    x=df[["Yesterday Close","Yesterday High","Yesterday Low","Yesterday Volume","Today Open"]]
    y=df[["Today Close"]]
    X_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
    model=LinearRegression()
    model.fit(X_train,y_train)
    y_pred=model.predict(x_test)
    mae=mean_absolute_error(y_test,y_pred)
    print(f"Mean Absoloute Error        :{mae}")
    mse=mean_squared_error(y_test,y_pred)
    print(f"Mean Squared Error          :{mse}")
    r2score=r2_score(y_test,y_pred)
    print(f"R2 Score                    :{r2score}")
    return model