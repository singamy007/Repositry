from sklearn.tree import DecisionTreeClassifier

# Sample data (simplified symptom encoding)
# Features: [pressure, sensitivity_light, nausea, throbbing, one_side, tearing, forehead_face, sudden, duration_hours]
# Labels: 'Tension', 'Migraine', 'Cluster', 'Sinus'
X = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # No headache
    [1, 0, 0, 0, 0, 0, 0, 0, 1],  # Tension
    [0, 1, 1, 1, 1, 0, 0, 0, 1],  # Migraine
    [0, 0, 0, 0, 1, 1, 0, 1, 0],  # Cluster
    [0, 0, 0, 0, 0, 1, 1, 0, 1],  # Sinus
]

y = [ "No headache","Tension", "Migraine", "Cluster", "Sinus"]

# Train the model
model = DecisionTreeClassifier()
model.fit(X, y)

# Collect user info
print("📝 Please enter your details:")
name_input = input("Enter your name: ")
age_input = input("Enter your age: ")
contact = input("Enter your contact number: ")

# Convert age to int
age = int(age_input)

# Determine proper name title
if age > 20:
    # Ask user how they identify (for Mr./Miss)
    gender_title = input("Do you prefer to be addressed as Mr. or Miss? ").strip().title()
    titled_name = f"{gender_title} {name_input}"
else:
    titled_name = name_input  # Just use the name for age <= 20

# Ask questions with personalized name
def ask(question):
    while True:
        try:
            response = input(f"{titled_name}, {question} (yes=1 / no=0): ").strip()
            answer = int(response)
            if answer in [0, 1]:
                return answer
            print("❌ Please enter either 1 for yes or 0 for no.")
        except ValueError:
            print("❌ Please enter either 1 for yes or 0 for no.")

print(f"\n🤖 {titled_name}, please answer the following:\n")


print("\n🤖 Answer the following to identify your headache type using AI:\n")

features = [
    ask("Do you feel a tight pressure around your head?"),
    ask("Are you sensitive to light or sound?"),
    ask("Do you feel nauseous?"),
    ask("Is the pain throbbing or pulsing?"),
    ask("Is the pain only on one side of the head?"),
    ask("Do you experience tearing or nasal congestion?"),
    ask("Is the pain in your forehead or face area?"),
    ask("Did the headache start suddenly and severely?"),
    ask("Does the headache last for several hours or days?")
]

# Predict
prediction = model.predict([features])# Make sure to wrap features in a list,this fun
print(f"\n🧠: Your headache type might be {prediction[0]},{titled_name}")
print("\n🧾 Summary of Your Input:")
print(f"👤 Name: {titled_name}")
print(f"🎂 Age: {age}")
print(f"📞 Contact: {contact}")
print("⚠️ Please consult a healthcare professional for a proper diagnosis.\n")