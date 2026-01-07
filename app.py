import json
import re
import math
from datetime import datetime
from collections import Counter
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class CustomVectorizer:
    """Custom TF-IDF implementation without using sklearn"""
    
    def __init__(self):
        self.vocabulary = {}  # word -> index mapping
        self.idf_values = {}  # word -> IDF score
        self.documents = []   # store original documents
        
    def _tokenize(self, text):
        """Convert text to lowercase and split into words"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
        words = text.split()
        # Remove common stop words manually
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                     'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were', 
                     'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 
                     'did', 'will', 'would', 'could', 'should', 'may', 'might',
                     'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
                     'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when',
                     'where', 'why', 'how'}
        return [w for w in words if w not in stop_words and len(w) > 1]
    
    def _calculate_tf(self, words):
        """Calculate Term Frequency for a document"""
        word_count = len(words)
        word_freq = Counter(words)
        tf_scores = {}
        for word, count in word_freq.items():
            tf_scores[word] = count / word_count
        return tf_scores
    
    def _calculate_idf(self):
        """Calculate Inverse Document Frequency for all words"""
        num_docs = len(self.documents)
        word_doc_count = {}
        
        # Count how many documents contain each word
        for doc in self.documents:
            unique_words = set(doc)
            for word in unique_words:
                word_doc_count[word] = word_doc_count.get(word, 0) + 1
        
        # Calculate IDF: log(total_docs / docs_containing_word)
        for word, doc_count in word_doc_count.items():
            self.idf_values[word] = math.log(num_docs / doc_count)
    
    def fit_transform(self, texts):
        """Train on documents and return TF-IDF vectors"""
        # Tokenize all documents
        self.documents = [self._tokenize(text) for text in texts]
        
        # Build vocabulary
        all_words = set()
        for doc in self.documents:
            all_words.update(doc)
        
        self.vocabulary = {word: idx for idx, word in enumerate(sorted(all_words))}
        
        # Calculate IDF values
        self._calculate_idf()
        
        # Create TF-IDF vectors for all documents
        vectors = []
        for doc in self.documents:
            vectors.append(self._create_vector(doc))
        
        return vectors
    
    def transform(self, texts):
        """Transform new texts to TF-IDF vectors"""
        vectors = []
        for text in texts:
            words = self._tokenize(text)
            vectors.append(self._create_vector(words))
        return vectors
    
    def _create_vector(self, words):
        """Create TF-IDF vector for a document"""
        # Initialize vector with zeros
        vector = [0.0] * len(self.vocabulary)
        
        # Calculate TF for this document
        tf_scores = self._calculate_tf(words)
        
        # Calculate TF-IDF for each word
        for word, tf in tf_scores.items():
            if word in self.vocabulary:
                idx = self.vocabulary[word]
                idf = self.idf_values.get(word, 0)
                vector[idx] = tf * idf
        
        return vector


def cosine_similarity_manual(vec1, vec2):
    """Calculate cosine similarity between two vectors manually"""
    # Dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Magnitude of vec1
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    
    # Magnitude of vec2
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    # Cosine similarity
    return dot_product / (magnitude1 * magnitude2)


class UniversityChatbot:
    """Custom chatbot built from scratch without AI libraries"""
    
    def __init__(self):
        self.vectorizer = CustomVectorizer()  # Our custom vectorizer
        self.knowledge_base = []
        self.question_vectors = []
        self.is_trained = False
        self.conversation_history = []
        
    def add_data(self, data_dict):
        """Add data to the knowledge base"""
        print("📚 Loading university data...")
        for category, qa_pairs in data_dict.items():
            for qa in qa_pairs:
                self.knowledge_base.append({
                    'category': category,
                    'question': qa['question'],
                    'answer': qa['answer']
                })
        print(f"✅ Loaded {len(self.knowledge_base)} Q&A pairs")
    
    def train(self):
        """Train the chatbot on the collected data"""
        if not self.knowledge_base:
            return False
        
        print("🤖 Training chatbot (custom implementation)...")
        questions = [item['question'] for item in self.knowledge_base]
        
        # Use our custom vectorizer instead of sklearn
        self.question_vectors = self.vectorizer.fit_transform(questions)
        
        self.is_trained = True
        print(f"✅ Chatbot trained on {len(self.knowledge_base)} Q&A pairs")
        return True
    
    def preprocess_text(self, text):
        """Preprocess input text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def find_best_match(self, user_question):
        """Find the best matching question manually"""
        if not self.is_trained:
            return {
                "answer": "Chatbot is not trained yet.",
                "similarity_score": 0.0,
                "matched_question": None
            }
        
        # Convert user question to vector using our custom vectorizer
        user_vector = self.vectorizer.transform([user_question])[0]
        
        # Manually calculate similarity with each stored question
        similarities = []
        for stored_vector in self.question_vectors:
            sim = cosine_similarity_manual(user_vector, stored_vector)
            similarities.append(sim)
        
        # Find the best match manually
        best_match_idx = 0
        best_score = similarities[0]
        for i, score in enumerate(similarities):
            if score > best_score:
                best_score = score
                best_match_idx = i
        
        # Log the interaction
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'question': user_question,
            'best_match': self.knowledge_base[best_match_idx]['question'],
            'similarity_score': float(best_score)
        })
        
        # Return answer if similarity is good enough
        if best_score > 0.3:
            return {
                "answer": self.knowledge_base[best_match_idx]['answer'],
                "similarity_score": float(best_score),
                "matched_question": self.knowledge_base[best_match_idx]['question'],
                "category": self.knowledge_base[best_match_idx]['category']
            }
        else:
            return {
                "answer": "I'm sorry, I don't have information about that. Please contact the university administration for more details.",
                "similarity_score": float(best_score),
                "matched_question": None,
                "category": None
            }
    
    def get_stats(self):
        """Get chatbot statistics"""
        avg_similarity = 0
        if self.conversation_history:
            total = sum(h['similarity_score'] for h in self.conversation_history)
            avg_similarity = total / len(self.conversation_history)
        
        return {
            "total_questions": len(self.conversation_history),
            "knowledge_base_size": len(self.knowledge_base),
            "avg_similarity": avg_similarity,
            "is_trained": self.is_trained,
            "vocabulary_size": len(self.vectorizer.vocabulary)
        }
    
    def get_topics(self):
        """Get available topics"""
        categories = {}
        for item in self.knowledge_base:
            category = item['category']
            if category not in categories:
                categories[category] = []
            categories[category].append({
                'question': item['question'],
                'answer': item['answer']
            })
        return categories


def create_sample_data():
    """Create sample university data"""
    return {
       
    }


# Initialize chatbot with custom implementation

chatbot = UniversityChatbot()

with open("university_data.json", "r") as file:
    data = json.load(file)

chatbot.add_data(data)
chatbot.train()


# API Routes
@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_question = data.get('question', '')
        
        if not user_question:
            return jsonify({"error": "No question provided"}), 400
        
        response = chatbot.find_best_match(user_question)
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get chatbot statistics"""
    try:
        stats = chatbot.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get available topics"""
    try:
        topics = chatbot.get_topics()
        return jsonify(topics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        return jsonify(chatbot.conversation_history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "is_trained": chatbot.is_trained,
        "knowledge_base_size": len(chatbot.knowledge_base),
        "implementation": "Custom (No AI Libraries)"
    }), 200


@app.route('/api/add_data', methods=['POST'])
def add_data():
    """Add new data to knowledge base"""
    try:
        data = request.get_json()
        chatbot.add_data(data)
        chatbot.train()
        return jsonify({"message": "Data added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 University Chatbot API Server")
    print("   (Custom Implementation - No AI Libraries)")
    print("="*60)
    print(f"✅ Chatbot trained with {len(chatbot.knowledge_base)} Q&A pairs")
    print(f"✅ Vocabulary size: {len(chatbot.vectorizer.vocabulary)} words")
    print("📡 Server running on http://localhost:5000")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)

    