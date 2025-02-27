import neptune
import xgboost as xgb
from neptune.integrations.xgboost import NeptuneCallback
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

# Create run
run = neptune.init_run(
    project="common/xgboost-integration",
    api_token=neptune.ANONYMOUS_API_TOKEN,
    name="xgb-cv",
    tags=["xgb-integration", "cv"],
)

# Create neptune callback
neptune_callback = NeptuneCallback(run=run, log_tree=[0, 1, 2, 3])

# Prepare data
X, y = fetch_california_housing(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
dtrain = xgb.DMatrix(X_train, label=y_train)
dval = xgb.DMatrix(X_test, label=y_test)

# Define parameters
model_params = {
    "eta": 0.7,
    "gamma": 0.001,
    "max_depth": 9,
    "objective": "reg:squarederror",
    "eval_metric": ["mae", "rmse"],
}
evals = [(dtrain, "train"), (dval, "valid")]
num_round = 57

# Run cross validation and log metadata to the run in Neptune
xgb.cv(
    params=model_params,
    dtrain=dtrain,
    num_boost_round=num_round,
    nfold=7,
    callbacks=[neptune_callback],
)
