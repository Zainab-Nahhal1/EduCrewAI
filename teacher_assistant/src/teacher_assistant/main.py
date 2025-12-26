"""
Main entry point for the Teacher Assistant Crew.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from teacher_assistant.crew import TeacherAssistantCrew

# Load environment variables
load_dotenv()


def check_environment():
    """Check if required environment variables are set."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-openai-api-key-here":
        print("\n" + "="*80)
        print("❌ ERROR: API Key Not Configured!")
        print("="*80)
        print("\nPlease set your API key in a .env file or environment variable:")
        print("OPENAI_API_KEY=YOUR_API_KEY_HERE\n")
        sys.exit(1)


def read_notes_from_file(file_path: str) -> str:
    """Read teaching notes from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            print(f"❌ ERROR: File '{file_path}' is empty!")
            sys.exit(1)
        
        return content
    
    except FileNotFoundError:
        print(f"❌ ERROR: File '{file_path}' not found!")
        print("Please create the file or check the file path.")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ ERROR: Could not read file: {e}")
        sys.exit(1)


def get_user_input() -> str:
    """Get teaching notes from user input."""
    print("\n" + "="*80)
    print("📝 ENTER YOUR TEACHING NOTES")
    print("="*80)
    print("\nPlease enter your teaching notes below.")
    print("Include: topic, grade level, key concepts, objectives, etc.")
    print("\nType your notes (press Enter twice when done, or Ctrl+D/Ctrl+Z+Enter):")
    print("-"*80)
    
    lines = []
    empty_line_count = 0
    
    try:
        while True:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
                if empty_line_count >= 2:  # Two empty lines = done
                    break
                lines.append(line)
            else:
                empty_line_count = 0
                lines.append(line)
    except EOFError:
        pass  # Ctrl+D/Ctrl+Z pressed
    
    notes = "\n".join(lines).strip()
    
    if not notes:
        print("\n❌ ERROR: No notes provided!")
        sys.exit(1)
    
    return notes


def save_results(result, output_file: str = "output/teacher_assistant_results.txt"):
    """Save the crew results to a file."""
    output_dir = Path(output_file).parent
    output_dir.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("TEACHER ASSISTANT CREW - RESULTS\n")
        f.write("="*80 + "\n\n")
        f.write(str(result))
        f.write("\n\n" + "="*80 + "\n")
        f.write("End of Results\n")
        f.write("="*80 + "\n")
    
    return output_file


def run():
    """
    Run the crew with user input or file.
    
    Usage:
        python -m teacher_assistant.main                  # Interactive input
        python -m teacher_assistant.main notes.txt        # From file
        python -m teacher_assistant.main --example        # Use example notes
    """
    print("\n" + "="*80)
    print("🎓 TEACHER ASSISTANT CREW")
    print("="*80)
    
    # Check environment
    check_environment()
    print("✓ Environment configured\n")
    
    # Determine input method
    notes = None
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--example":
            # Use example notes
            print("📚 Using example notes (Photosynthesis)")
            notes = """
Topic: Introduction to Photosynthesis

Grade Level: 7th Grade Life Science

Key Concepts:
- Photosynthesis is the process plants use to convert light energy into chemical energy
- Chemical equation: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2
- Takes place in chloroplasts, specifically in chlorophyll
- Two main stages: light-dependent reactions and light-independent reactions (Calvin Cycle)
- Light-dependent reactions occur in thylakoid membranes
- Calvin Cycle occurs in the stroma
- Factors affecting photosynthesis: light intensity, CO2 concentration, temperature

Learning Objectives:
- Students will explain the process of photosynthesis
- Students will identify the reactants and products
- Students will describe the role of chlorophyll and chloroplasts
- Students will analyze how environmental factors affect photosynthesis rates

Prior Knowledge:
- Basic cell structure (organelles)
- Chemical equations basics
- Understanding of energy concepts
- Plant cell anatomy

Real-World Connections:
- Food production and agriculture
- Oxygen in Earth's atmosphere
- Climate change and carbon cycle
- Renewable energy and biomass
"""
        else:
            # Read from file
            notes_file = arg
            print(f"📖 Reading notes from: {notes_file}")
            notes = read_notes_from_file(notes_file)
            print(f"✓ Loaded {len(notes)} characters ({len(notes.split())} words)")
    else:
        # Interactive input
        notes = get_user_input()
        print(f"\n✓ Received {len(notes)} characters ({len(notes.split())} words)")
    
    print("="*80)
    
    # Preview notes
    print("\n📋 NOTES PREVIEW:")
    print("-"*80)
    preview = notes[:300] + "..." if len(notes) > 300 else notes
    print(preview)
    print("-"*80)
    
    # Confirm
    print("\n⚠️  Generating teaching materials based on these notes.")
    print("This will take 3-5 minutes.")
    
    confirm = input("\nProceed? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("\n❌ Cancelled by user.")
        sys.exit(0)
    
    # Create the crew
    print("\nInitializing agents...")
    inputs = {'notes': notes}
    
    try:
        crew_instance = TeacherAssistantCrew()
        print("✓ Crew initialized successfully")
        
        # Run the crew
        print("\n🚀 Starting Crew Execution...")
        print("⏱️  This will take 3-5 minutes. Please wait...")
        print("\n" + "-"*80 + "\n")
        
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Save results
        print("\n" + "="*80)
        print("✨ CREW EXECUTION COMPLETED!")
        print("="*80)
        
        output_file = save_results(result)
        
        print(f"\n💾 Results saved to: {output_file}")
        print("\n📊 Generated Materials:")
        print("   ✓ Comprehensive Lesson Plan")
        print("   ✓ Assessment Quiz with Answer Key")
        print("   ✓ Detailed Teaching Strategies & Suggestions")
        print("\n🎉 Your teaching materials are ready!")
        print(f"\nOpen the file to view: {os.path.abspath(output_file)}")
        print("="*80 + "\n")
        
    except Exception as e:
        import traceback
        print(f"\n❌ ERROR: An error occurred during execution:")
        print(f"{str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        print("\nPlease check your configuration and try again.")
        sys.exit(1)


def train():
    """Train the crew for a given number of iterations."""
    print("\n🎯 Training Mode")
    print("="*80)
    
    if len(sys.argv) < 3:
        print("Usage: python -m teacher_assistant.main train <iterations> <filename>")
        sys.exit(1)
    
    n_iterations = int(sys.argv[2])
    filename = sys.argv[3]
    
    inputs = {
        'notes': """
Topic: Introduction to Fractions
Key Concepts: numerator, denominator, parts of a whole
Grade: 4th Grade Mathematics
"""
    }
    
    try:
        print(f"Training for {n_iterations} iterations...")
        print(f"Training data will be saved to: {filename}")
        
        TeacherAssistantCrew().crew().train(
            n_iterations=n_iterations,
            filename=filename,
            inputs=inputs
        )
        
        print("\n✓ Training completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Training error: {e}")
        sys.exit(1)


def replay():
    """Replay the crew execution from a specific task."""
    print("\n🔄 Replay Mode")
    print("="*80)
    
    if len(sys.argv) < 3:
        print("Usage: python -m teacher_assistant.main replay <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[2]
    
    try:
        print(f"Replaying task: {task_id}")
        TeacherAssistantCrew().crew().replay(task_id=task_id)
        print("\n✓ Replay completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Replay error: {e}")
        sys.exit(1)


def test():
    """Test the crew execution and return results."""
    print("\n🧪 Test Mode")
    print("="*80)
    
    if len(sys.argv) < 4:
        print("Usage: python -m teacher_assistant.main test <iterations> <model>")
        sys.exit(1)
    
    n_iterations = int(sys.argv[2])
    model_name = sys.argv[3]
    
    inputs = {
        'notes': """
Topic: Basic Fractions
Objectives: Understand numerator and denominator, compare fractions
Grade: 4th Grade
"""
    }
    
    try:
        print(f"Testing for {n_iterations} iterations with {model_name}...")
        
        TeacherAssistantCrew().crew().test(
            n_iterations=n_iterations,
            openai_model_name=model_name,
            inputs=inputs
        )
        
        print("\n✓ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Check for command mode
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "train":
            train()
        elif command == "replay":
            replay()
        elif command == "test":
            test()
        elif command == "--example":
            run()
        else:
            # Assume it's a file path
            run()
    else:
        # Default mode - interactive user input
        run()