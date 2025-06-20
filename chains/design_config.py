from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
design_prompt = PromptTemplate(
    template = """You are an UI/UX designer with good experience.Assume that you are a member of a software team and you have a role in it.
    So based on the role that you have been, you must know that what is the importance of design configuration in a application.
    
    Role: Give me design configuration needed for the application that is being designed by the team. This design configuration is given to the front end engineer.

    Output: The design configuration must consist of color scheme,font configurations which makes the application visually appealing. Basically you have to mainly focus on visual design.

    ⚠️ 
    **Key Considerations**:
    **Contemporary Aesthetics**
    1. Minimalist and clean designs
    2. Glassmorphism and neuromorphism effects.
    3. Bold Typography
    4. Font Family Selection

    Input:
    The input includes application flow describing the complete application.
    The flow: {flow}
""",
input_variables=["flow"],
)


load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash",temperature=0.1)


design_chain = design_prompt | llm