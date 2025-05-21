from pydantic import BaseModel, Field



class SaveAnswerRate(BaseModel):
    """
        Use this tool for save answer rate
    """

    score: float = Field(description="Score of the answer (0-5)")
    feedback: str = Field(description="Feedback of the answer")
    answer_id: str = Field(description="For which answer is returned rate, id in UUID format")

    async def execute(self):
        return self.model_dump()

    @classmethod
    def to_function_definition(cls):
        return {
            "name": cls.__name__,
            "description": cls.__doc__,
            "parameters": cls.model_json_schema(),
        }
