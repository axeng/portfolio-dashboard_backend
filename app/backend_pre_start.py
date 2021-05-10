from tenacity import retry, stop_after_attempt, wait_fixed

from app.database import SessionLocal

# Source https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/backend_pre_start.py

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds)
)
def init() -> None:
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
    except Exception as e:
        raise e


def main() -> None:
    init()


if __name__ == "__main__":
    main()
