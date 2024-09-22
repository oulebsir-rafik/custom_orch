from tasks import PyTask
from dag import DAG


def hello_world(message: str) -> None:
    print(message)


def hello_earth(message: str) -> None:
    print(f"Hello Earth! {message}")


def hello_mars(message: str) -> None:
    print(f"Hello Mars! {message}")


if __name__ == "__main__":
    with DAG() as dag:
        task_first = PyTask(hello_world)
        task_second = PyTask(hello_mars)
        task_third = PyTask(hello_earth)

        task_first >> task_second >> task_third
