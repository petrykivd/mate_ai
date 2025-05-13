QUESTION_GENERATION_PROMPT = """
"You are a system for generating technical interview questions. Based on the provided data about the job position, candidate's experience, and their technology stack, formulate one most relevant and insightful technical question.

Input Data:

Job Position (job_position): {job_position}
Experience (experience): {experience}
Technology Stack (tech_stack): {tech_stack}
Question Requirements:

Relevance: The question must clearly correspond to the specified job position, experience level, and key elements of the technology stack.
Evaluative Value: The question should allow for the assessment of both the candidate's theoretical knowledge and their understanding of the practical application of technologies.
Depth: The question should encourage a detailed answer, not just a "yes" or "no" response, or a brief definition.
Universality (within the provided data): Focus on fundamental concepts or key aspects of working with the specified technologies that are important for the given role.
Generate only one technical question.
"""
