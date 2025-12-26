from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from teacher_assistant.tools.custom_tool import NotesAnalysisTool, GradeLevelAnalyzer
import os
import yaml


@CrewBase
class TeacherAssistantCrew:
    """Teacher Assistant crew for generating educational materials."""
    
    # Get the directory containing this file
    _project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build paths to config files
    _agents_path = os.path.join(_project_dir, "config", "agents.yaml")
    _tasks_path = os.path.join(_project_dir, "config", "tasks.yaml")
    
    # Use custom names that CrewAI won't overwrite
    with open(_agents_path, "r", encoding="utf-8") as f:
        _agents_data = yaml.safe_load(f)
    
    with open(_tasks_path, "r", encoding="utf-8") as f:
        _tasks_data = yaml.safe_load(f)
    
    print(f"✓ Class level - Loaded agents: {list(_agents_data.keys())}")
    print(f"✓ Class level - Loaded tasks: {list(_tasks_data.keys())}")
    
    # Initialize tools at class level
    notes_analyzer = NotesAnalysisTool()
    grade_analyzer = GradeLevelAnalyzer()
    
    @agent
    def lesson_plan_agent(self) -> Agent:
        """Create the lesson plan architect agent."""
        config = self._agents_data['lesson_plan_agent']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            tools=[self.notes_analyzer, self.grade_analyzer],
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def quiz_generator_agent(self) -> Agent:
        """Create the quiz generator agent."""
        config = self._agents_data['quiz_generator_agent']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def teaching_strategy_agent(self) -> Agent:
        """Create the teaching strategy agent."""
        config = self._agents_data['teaching_strategy_agent']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            tools=[self.notes_analyzer],
            verbose=True,
            allow_delegation=False
        )
    
    @task
    def generate_lesson_plan(self) -> Task:
        """Task to generate a comprehensive lesson plan."""
        config = self._tasks_data['generate_lesson_plan']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.lesson_plan_agent()
        )
    
    @task
    def generate_quiz(self) -> Task:
        """Task to generate an assessment quiz."""
        config = self._tasks_data['generate_quiz']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.quiz_generator_agent(),
            context=[self.generate_lesson_plan()]
        )
    
    @task
    def generate_teaching_suggestions(self) -> Task:
        """Task to generate teaching strategies and suggestions."""
        config = self._tasks_data['generate_teaching_suggestions']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.teaching_strategy_agent(),
            context=[self.generate_lesson_plan(), self.generate_quiz()]
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Teacher Assistant crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )