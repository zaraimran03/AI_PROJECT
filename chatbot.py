
import json
import os

class UniversityChatbot:
    def __init__(self):
        # File where knowledge is stored
        self.knowledge_file = "university_data.json"
        
        # Load the knowledge when chatbot starts
        self.knowledge = self.load_knowledge()
        
        # Store conversation history
        self.conversation_history = []
        
        print("🤖 University Chatbot Initialized!")
        print(f"📚 Loaded {self.count_questions()} questions")
    
    def load_knowledge(self):
        """Load questions and answers from JSON file"""
        # Check if file exists
        if os.path.exists(self.knowledge_file):
            try:
                # Open and read the file
                with open(self.knowledge_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                print(f"✅ Successfully loaded from {self.knowledge_file}")
                return data
            except Exception as e:
                print(f"❌ Error loading file: {e}")
                # If error, use default data
                return self.create_default_data()
        else:
            print("📝 Creating new knowledge base file...")
            return self.create_default_data()
    

        

    
    def save_knowledge(self, data):
        """Save knowledge to JSON file"""
        try:
            with open(self.knowledge_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
            print(f"💾 Knowledge saved to {self.knowledge_file}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    
    def count_questions(self):
        """Count total number of questions"""
        total = 0
        for category in self.knowledge.values():
            total += len(category)
        return total
    
    def clean_text(self, text):
        """Clean and prepare text for matching"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra spaces
        text = ' '.join(text.split())
        return text
    
    def find_best_answer(self, user_question):
        """Find the best answer for user's question"""
        clean_question = self.clean_text(user_question)
        
        # Split question into words
        user_words = set(clean_question.split())
        
        best_answer = None
        best_match_count = 0
        
        # Search through all categories
        for category, qa_list in self.knowledge.items():
            for qa in qa_list:
                # Get question words
                question_words = set(qa["question"].split())
                
                # Count matching words
                match_count = len(user_words.intersection(question_words))
                
                # If this is better match, save it
                if match_count > best_match_count:
                    best_match_count = match_count
                    best_answer = qa["answer"]
        
        return best_answer, best_match_count
    
    def add_to_history(self, question, answer):
        """Add conversation to history"""
        self.conversation_history.append({
            "question": question,
            "answer": answer,
            "timestamp": "Now"  # You can add actual time if needed
        })
    
    def show_help(self):
        """Display help information"""
        help_text = """
📖 **UNIVERSITY CHATBOT HELP MENU**
===================================

I can help you with information about:

🎓 **COURSES** - Academic programs and classes
   • Computer Science courses
   • Engineering programs
   • Business courses

📝 **ADMISSIONS** - Application process
   • Admission requirements
   • Application deadlines
   • How to apply

🏛️ **CAMPUS** - University facilities
   • Campus location
   • Library hours
   • Campus facilities

💰 **FINANCIAL** - Fees and scholarships
   • Scholarships available
   • Tuition fees
   • Financial aid

🔧 **AVAILABLE COMMANDS:**
   • 'help' - Show this help menu
   • 'topics' - List all available topics
   • 'stats' - Show chatbot statistics
   • 'quit' - Exit the chatbot

💡 **EXAMPLE QUESTIONS:**
   • "What computer science courses are available?"
   • "What are the admission requirements?"
   • "When is the application deadline?"
   • "Where is the campus located?"
   • "What scholarships are available?"

===================================
        """
        return help_text
    
    def show_topics(self):
        """Display all available topics"""
        topics_text = "\n📚 **AVAILABLE TOPICS:**\n"
        topics_text += "=" * 30 + "\n"
        
        for category, qa_list in self.knowledge.items():
            topics_text += f"\n{category.upper()}:\n"
            topics_text += "-" * 20 + "\n"
            for qa in qa_list:
                topics_text += f"  • {qa['question']}\n"
        
        return topics_text
    
    def show_stats(self):
        """Display chatbot statistics"""
        total_questions = self.count_questions()
        categories = len(self.knowledge)
        conversations = len(self.conversation_history)
        
        stats_text = f"""
📊 **CHATBOT STATISTICS:**
=========================

• Total Questions in Knowledge Base: {total_questions}
• Number of Categories: {categories}
• Conversation History: {conversations} exchanges
• Knowledge File: {self.knowledge_file}

**Categories Available:**
"""
        for category in self.knowledge.keys():
            count = len(self.knowledge[category])
            stats_text += f"  • {category.title()}: {count} questions\n"
        
        return stats_text
    
    def start_chat(self):
        """Start the chatbot conversation"""
        print("\n" + "="*60)
        print("🎓 WELCOME TO UNIVERSITY INFORMATION CHATBOT")
        print("="*60)
        print("🤖 I'm here to help you with university information!")
        print("💡 Type 'help' to see what I can do")
        print("👋 Type 'quit' to exit the chatbot")
        print("-" * 60 + "\n")
        
        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                # Check for empty input
                if not user_input:
                    print("🤔 Please type a question or command...")
                    continue
                
                # Check for commands
                if user_input.lower() == 'quit':
                    print("\n🙏 Thank you for using University Chatbot!")
                    print("🎓 Have a great day!\n")
                    break
                
                elif user_input.lower() == 'help':
                    print(self.show_help())
                
                elif user_input.lower() == 'topics':
                    print(self.show_topics())
                
                elif user_input.lower() == 'stats':
                    print(self.show_stats())
                
                else:
                    # Try to find answer
                    answer, match_count = self.find_best_answer(user_input)
                    
                    if answer and match_count > 0:
                        print(f"\n🤖 Bot: {answer}")
                        self.add_to_history(user_input, answer)
                        
                        # Show match quality
                        if match_count >= 3:
                            print("   ✅ Good match!")
                        elif match_count == 2:
                            print("   ⚠️  Partial match")
                        else:
                            print("   ℹ️  Basic match")
                    else:
                        print("\n🤖 Bot: I'm sorry, I don't have information about that.")
                        print("   💡 Try asking about:")
                        for category in self.knowledge.keys():
                            print(f"      • {category.title()}")
                        print("   🆘 Type 'help' for more options")
                
                print()  # Empty line for readability
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("   🔧 Please try again or type 'quit' to exit")

# Main function to run the chatbot
def main():
    """Main function that runs when the script starts"""
    print("🚀 Starting University Chatbot System...")
    
    # Create chatbot instance
    chatbot = UniversityChatbot()
    
    # Start chatting
    chatbot.start_chat()
    
    print("✅ Chatbot session ended.")

# This makes sure the chatbot runs when we execute the file
if __name__ == "__main__":
    main()