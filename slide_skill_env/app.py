"""FastAPI application for the Slide Skill environment."""

from openenv.core.env_server.http_server import create_app

from slide_skill_env.models import SkillAction, SkillObservation
from slide_skill_env.slide_skill_environment import SlideSkillEnvironment

app = create_app(
    SlideSkillEnvironment,
    SkillAction,
    SkillObservation,
    env_name="slide_skill",
)


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
