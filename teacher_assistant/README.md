# Teacher Assistant Crew

An AI-powered teaching assistant built with CrewAI that generates comprehensive lesson plans, assessment quizzes, and teaching strategies from your teaching notes.

## 🎯 Features

- **📚 Lesson Plan Generation**: Detailed plans with objectives, activities, timing, materials, and assessment strategies
- **📝 Quiz Generation**: Comprehensive assessments with multiple question types and complete answer keys
- **💡 Teaching Strategies**: Engagement tactics, misconceptions, differentiation, and practical classroom tips
- **🛠️ Custom Tools**: Built-in note analysis and grade level assessment tools

## 📁 Project Structure

```
teacher_assistant/
├── .env                    # Environment variables (API keys)
├── pyproject.toml          # Project configuration
├── README.md               # This file
└── src/
    └── teacher_assistant/
        ├── __init__.py
        ├── main.py         # Entry point
        ├── crew.py         # Crew definition
        ├── config/
        │   ├── agents.yaml # Agent configurations
        │   └── tasks.yaml  # Task configurations
        └── tools/
            ├── __init__.py
            └── custom_tools.py  # Custom analysis tools
```

## 🚀 Installation

### Step 1: Create Virtual Environment

```powershell
# Navigate to your project directory
cd teacher_assistant

# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
```

### Step 2: Install Dependencies

```powershell
pip install crewai crewai-tools python-dotenv
```

Or install in development mode:

```powershell
pip install -e .
```

### Step 3: Configure API Key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
OPENAI_MODEL_NAME=gpt-4o-mini
```

## 💻 Usage

### Method 1: Run with Default Example

```powershell
python -m teacher_assistant.main
```

This will process the built-in example about Photosynthesis.

### Method 2: Run with Your Notes File

```powershell
python -m teacher_assistant.main notes.txt
```

Or with full path:

```powershell
python -m teacher_assistant.main "C:\path\to\your\notes.txt"
```

### Method 3: Train the Crew

```powershell
python -m teacher_assistant.main train 5 training_data.json
```

### Method 4: Replay a Task

```powershell
python -m teacher_assistant.main replay <task_id>
```

### Method 5: Test the Crew

```powershell
python -m teacher_assistant.main test 2 gpt-4
```

## 📝 Notes File Format

Create a text file with your teaching content:

```txt
Topic: Introduction to [Your Topic]

Grade Level: [Grade]

Key Concepts:
- Concept 1
- Concept 2
- Concept 3

Learning Objectives:
- Students will understand...
- Students will be able to...

Prior Knowledge:
- What students should already know

Real-World Connections:
- How this applies to real life

Vocabulary:
- Term 1, Term 2, Term 3
```

## 📤 Output

Results are saved to `output/teacher_assistant_results.txt` and include:

1. **Complete Lesson Plan** (1500-2000 words)
   - Header with title, subject, grade, duration
   - 3-5 clear learning objectives
   - Materials and resources
   - Detailed activities with timing (warm-up, instruction, practice, closure)
   - Assessment strategies
   - Differentiation approaches
   - Teacher notes and tips

2. **Assessment Quiz** (1000-1500 words)
   - 3 multiple choice questions (30 points)
   - 3 short answer questions (30 points)
   - 2-4 problem-solving questions (40 points)
   - Complete answer key with explanations
   - Grading rubric
   - Point distributions

3. **Teaching Strategies Guide** (2000-2500 words)
   - 5-6 engagement strategies
   - 4-5 common misconceptions with corrections
   - Differentiation for all learner types
   - 4-5 real-world applications
   - Additional resources (websites, videos, activities, books)
   - Classroom management tips
   - Formative assessment techniques
   - Technology integration ideas

## 🛠️ Custom Tools

The crew includes two custom tools:

### NotesAnalysisTool
Analyzes teaching notes to extract:
- Subject area identification
- Grade level detection
- Key concepts extraction
- Learning objectives parsing
- Vocabulary terms
- Prior knowledge requirements
- Real-world connections

### GradeLevelAnalyzer
Analyzes content complexity and suggests appropriate grade levels based on:
- Average word length
- Average sentence length
- Vocabulary complexity

## ⚙️ Configuration

### Modify Agents

Edit `src/teacher_assistant/config/agents.yaml` to customize:
- Agent roles and goals
- Agent backstories and expertise
- Agent behavior and focus

### Modify Tasks

Edit `src/teacher_assistant/config/tasks.yaml` to customize:
- Task descriptions and requirements
- Expected output format and length
- Context and dependencies

### Change AI Model

Edit `.env`:
```env
OPENAI_MODEL_NAME=gpt-4  # or gpt-4-turbo, gpt-3.5-turbo
```

## 🔧 Troubleshooting

### "No module named 'crewai'"
```powershell
pip install crewai crewai-tools
```

### "No module named 'teacher_assistant'"
Make sure you're in the project directory and run:
```powershell
pip install -e .
```

### "API key not configured"
Check that `.env` file exists and contains your actual API key.

### Slow execution
The crew takes 3-5 minutes to complete. This is normal as it generates comprehensive, high-quality materials.

## 📊 Example Output Structure

```
LESSON PLAN
├── Header (Title, Subject, Grade, Duration)
├── Learning Objectives (3-5 objectives)
├── Materials & Resources
├── Activities
│   ├── Warm-up (5-10 min)
│   ├── Direct Instruction (15-20 min)
│   ├── Guided Practice (10-15 min)
│   ├── Independent Practice (10-15 min)
│   └── Closure (5 min)
├── Assessment Strategies
├── Differentiation
└── Teacher Notes

QUIZ
├── Multiple Choice Section (3 questions, 30 pts)
├── Short Answer Section (3 questions, 30 pts)
├── Problem Solving Section (2-4 questions, 40 pts)
├── Answer Key (with explanations)
└── Grading Rubric

TEACHING STRATEGIES
├── Engagement Strategies (5-6)
├── Common Misconceptions (4-5)
├── Differentiation
│   ├── Below Grade Level
│   ├── On Grade Level
│   ├── Above Grade Level
│   ├── ELL Students
│   └── Special Needs
├── Real-World Applications (4-5)
├── Additional Resources
│   ├── Websites
│   ├── Videos
│   ├── Activities
│   └── Books
├── Classroom Management Tips
├── Assessment Techniques
└── Technology Integration
```

## 🎓 Tips for Best Results

1. **Be Specific**: Include explicit grade levels and subject areas
2. **Add Context**: Mention what students already know
3. **List Objectives**: Clearly state what students should learn
4. **Include Vocabulary**: List important terms to teach
5. **Mention Challenges**: Note common misconceptions if known
6. **Add Applications**: Suggest real-world connections
7. **Be Detailed**: More detail in notes = better output

## 📚 Dependencies

- `crewai>=0.86.0` - AI agent orchestration framework
- `crewai-tools>=0.17.0` - Additional tools for CrewAI
- `python-dotenv>=1.0.0` - Environment variable management
- `openai` - OpenAI API client (installed with crewai)
- `pydantic` - Data validation (installed with crewai)

## 🤝 Contributing

Feel free to fork, modify, and extend this project for your needs!

## 📄 License

MIT License - Free to use and modify

## 🆘 Support

For issues with:
- **CrewAI**: https://docs.crewai.com
- **OpenAI API**: https://platform.openai.com/docs

## 🎉 Credits

Built with:
- **CrewAI** - Multi-agent orchestration
- **OpenAI GPT** - Language model
- **Python** - Programming language

