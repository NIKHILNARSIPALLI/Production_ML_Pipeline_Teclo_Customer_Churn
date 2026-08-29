from src.config import load_config

test_config = load_config()

print(test_config.unitTest.parameter1) # type: ignore