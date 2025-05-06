# Mental Health Support Application

## Overview
The Mental Health Support Application is a comprehensive, AI-powered platform designed to provide accessible mental health support through a conversational interface. This application leverages a multi-agent system powered by CrewAI and Mem0 to deliver personalized, empathetic, and evidence-based mental health guidance.

## Features

### User-Friendly Interface
- **Multi-page Streamlit Application**: Easy navigation between profile creation and chat interface
- **Clean, Intuitive Design**: Accessible for users of all technical abilities
- **Responsive Layout**: Works well on various devices and screen sizes

### Versatile Communication Options
- **Text-based Chat**: Traditional typing interface
- **Speech-to-Text**: Voice input capability for natural conversation
- **Speech-to-Speech**: Full voice interaction for accessible support

### Intelligent Multi-Agent System
- **Assistant Agent**: Empathetic conversational interface that assesses mental state through thoughtful dialogue
- **Summarizer Agent**: Tracks conversation context to maintain coherent support throughout the session
- **Expert Agent**: Provides evidence-based mental health guidance sourced from professional literature

### Knowledge Base
- Built on established mental health resources and research papers
- Includes evidence-based approaches for stress, anxiety, burnout, and depression management
- Knowledge derived from professional mental health literature

### Memory System
- Powered by Mem0 to maintain conversation context
- Personalized support based on user's history and profile
- Consistent experience across multiple sessions

### Privacy-focused
- User information is kept confidential
- Optional data sharing based on user preferences
- Transparent about data handling procedures

## Getting Started

### Prerequisites
- Python 3.9+
- Required Python packages (see Installation section)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mental-health-support-app.git
cd mental-health-support-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
MEM0_API_KEY=your_mem0_api_key
```

### Running the Application

1. Launch the Streamlit application:
```bash
streamlit run home.py
```

2. Navigate to the link provided in your terminal (typically http://localhost:8501)

3. Follow the on-screen instructions to create your profile and begin your support session

### Command Line Interface (Optional)

For a simplified, text-only experience, you can also run the command-line version:
```bash
python main.py
```

## Project Structure

```
├── home.py                       # Main entry point for the Streamlit app
├── main.py                       # Command-line interface version
├── pages/                        # Streamlit pages
│   ├── 1_user_form.py            # User profile creation page
│   └── 3_chatbot.py              # Chatbot interface page
├── src/                          # Source code
│   └── crewai_knowledge_chatbot/
│       └── crew.py               # CrewAI configuration
├── config/                       # Configuration files
│   ├── agents.yaml               # Agent definitions
│   └── tasks.yaml                # Task definitions
└── literature-review-stress-anxiety-burnout-and-depression-impact-on-teachers-and-on-learner-outcomes.pdf
└── manage_stress_workbook.pdf    # Knowledge sources
```

## Technical Implementation

### CrewAI Multi-Agent Framework
The application uses CrewAI to orchestrate a team of specialized agents:

1. **Assistant Agent**: Serves as the primary interface, conducting empathetic conversations with users.
2. **Summarizer Agent**: Processes conversation history to maintain context and provide coherent support.
3. **Expert Agent**: Draws on knowledge sources to provide evidence-based mental health guidance.

### Knowledge Integration
PDF knowledge sources provide the system with professional mental health resources:
- Research on stress, anxiety, burnout, and depression
- Evidence-based management techniques and strategies

### Memory Management
Mem0 provides persistent memory capabilities:
- Maintains conversation context across the session
- Enables personalized responses based on user history
- Creates a coherent support experience

## Contributing
Contributions to improve the Mental Health Support Application are welcome! Please feel free to submit pull requests or create issues for bugs, features, or improvements.

## License
[Insert your license information here]

## Disclaimer
This application is designed to provide supportive conversations and information about mental health. It is not a substitute for professional mental health care. If you are experiencing a mental health crisis, please contact a crisis helpline or seek help from a qualified healthcare professional.

## Acknowledgements
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [Mem0](https://github.com/getmemo/memo)
- [Streamlit](https://streamlit.io/)
- Mental health resources and research papers used in the knowledge base