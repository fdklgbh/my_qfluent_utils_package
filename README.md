# my_qfluent_utils_package

qfluent封装自用,便于调用

## windows 
### 1. CFluentWindow
去掉FluentWindow的返回按钮

## common
### 1.  CQConfig.py
CustomConfig

使用:

```python
class Config(CustomConfig):
    pass
user_cfg = Config()
user_cfg.load(YOUR_CONFIG_PATH, user_cfg)
```