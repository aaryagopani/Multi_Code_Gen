# from graph.main_graph import run_graph

# def main():
#     print("🔷 Welcome to the Web Project Idea Assistant!")
#     user_prompt = input("💬 Please enter your project idea or prompt:\n> ")
#     output = run_graph(user_prompt)
#     print("\n--- Thinker Agent Output ---\n")
#     print(output)

# if __name__ == "__main__":
#     main()

from graph.main_graph import run_graph

if __name__ == "__main__":
    
    user_idea = input("Enter your project idea: ")
    run_graph(user_idea)

