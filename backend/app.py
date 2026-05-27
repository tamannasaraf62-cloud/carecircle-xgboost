from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CareCircle Chatbot")


class ChatRequest(BaseModel):
    message: str


def has_phrase(msg, phrases):
    return any(phrase in msg for phrase in phrases)


def is_greeting(msg):
    greetings = [
        "hi", "hii","hyy", "hello", "hey", "namaste",
        "good morning", "good evening", "good afternoon"
    ]
    return msg in greetings


def chatbot_reply(message: str):
    msg = message.lower().strip()

    if msg == "":
        return "Please type your question. I can help with queue, appointment, doctors, rooms, billing, reports, and emergency support."

    # BASIC TALK
    if is_greeting(msg):
        return "Hello, welcome to CareCircle. How can I help you today?"

    elif has_phrase(msg, [
        "kaise ho", "kaise ho aap", "kese ho", "kaise hain",
        "how are you", "how r u", "how are u"
    ]):
        return "Main theek hoon, thank you. Aap batayiye, hospital service mein kis cheez ki help chahiye?"

    elif has_phrase(msg, [
        "who are you", "what are you", "about you",
        "tum kaun", "aap kaun"
    ]):
        return "I am CareCircle Assistant, a hospital support chatbot. I help patients with basic hospital services."

    elif has_phrase(msg, [
        "help", "menu", "services", "what can you do",
        "kya kar sakte", "kaise help"
    ]):
        return (
            "I can help with:\n"
            "- Emergency guidance\n"
            "- Queue/token status\n"
            "- Appointment support\n"
            "- Doctor or department suggestion\n"
            "- Room and hospital navigation\n"
            "- Billing, insurance, pharmacy, and lab report help"
        )

    elif has_phrase(msg, ["thank you", "thanks", "shukriya", "dhanyavaad"]):
        return "You’re welcome. Take care."

    elif has_phrase(msg, ["bye", "goodbye", "ok bye"]):
        return "Goodbye. Wishing you good health."

    # EMERGENCY
    elif has_phrase(msg, [
        "heart attack", "chest pain", "stroke", "seizure",
        "unconscious", "unconcious", "not breathing", "can't breathe",
        "saans nahi", "saans nhi", "saans nahi aa rahi",
        "behosh", "behoshi", "behosh ho rahi", "behosh ho raha",
        "chakkar", "chakkar aa rahe", "dizzy", "dizziness",
        "faint", "fainted", "fainting", "gir gaya", "gir gayi",
        "serious", "mar raha", "mar rahi"
    ]):
        return (
            "This sounds serious. Please do not wait in the normal queue. "
            "Go to the emergency ward immediately or call an ambulance."
        )

    elif has_phrase(msg, [
        "breathing problem", "asthma", "asthma attack",
        "accident", "heavy bleeding", "bleeding",
        "severe pain", "bahut dard", "blood nikal"
    ]):
        return (
            "This may need urgent attention. Please inform hospital staff immediately "
            "or visit the emergency desk."
        )

    elif has_phrase(msg, [
        "ambulance", "emergency number", "ambulance number", "emergency vehicle"
    ]):
        return "For ambulance support, please call 108 or contact the hospital emergency desk."

    # HOSPITAL / TIME
    elif has_phrase(msg, [
        "which hospital", "best hospital", "nearby hospital",
        "hospital kaha", "carecircle hospital", "hospital"
    ]):
        return (
            "CareCircle can help you with hospital services like appointments, "
            "queue tracking, emergency support, doctor guidance, billing, and navigation."
        )

    elif has_phrase(msg, [
        "how much time", "kitna time", "how long",
        "waiting time", "time lagega", "kab tak"
    ]):
        return (
            "Estimated waiting time depends on queue status and department. "
            "Current demo waiting time is around 20 minutes."
        )

    # REGISTRATION / TOKEN / QUEUE
    elif has_phrase(msg, [
        "register", "new patient", "patient registration",
        "registration", "naam likhna"
    ]):
        return (
            "Sure. For patient registration, please keep these details ready: "
            "name, age, gender, mobile number, and main health concern."
        )

    elif has_phrase(msg, [
        "generate token", "new token", "assign token",
        "give token", "token banana"
    ]):
        return (
            "Your demo token is CC-019. Department: General OPD. "
            "Estimated waiting time is around 20 minutes."
        )

    elif has_phrase(msg, [
        "queue", "wait", "waiting", "token", "turn",
        "doctor late", "doctor delay", "line", "mera number",
        "number kab", "kab ayega", "meri baari", "baari"
    ]):
        return (
            "Current token is 15. Your token is 19. "
            "There are 4 patients before you. Estimated wait time is around 20 minutes."
        )

    # APPOINTMENT
    elif has_phrase(msg, [
        "appointment", "book", "cancel", "reschedule",
        "schedule", "appointment lena", "doctor se milna", "booking"
    ]):
        return (
            "I can help with appointment support. Available demo slots are:\n"
            "1. Dr. Sharma - Cardiology - 10:00 AM\n"
            "2. Dr. Khan - Dermatology - 12:30 PM\n"
            "3. Dr. Patel - Orthopedics - 3:00 PM\n"
            "Please share doctor name and preferred time."
        )

    # DOCTOR / DEPARTMENT
    elif has_phrase(msg, [
        "which doctor", "which department", "konsa doctor",
        "kaun doctor", "doctor kaun", "doctor chahiye"
    ]):
        return "Please tell me the health issue, like heart, skin, bone, child care, or pregnancy, and I’ll suggest the department."

    elif has_phrase(msg, ["heart", "chest", "cardiologist", "cardio", "dil"]):
        return "For heart or chest-related problems, Cardiology is the right department. You can consult Dr. Sharma."

    elif has_phrase(msg, ["skin", "rash", "itching", "dermatologist", "khujli", "daane"]):
        return "For skin problems, Dermatology is suitable. You can consult Dr. Khan."

    elif has_phrase(msg, ["bone", "fracture", "joint", "orthopedic", "haddi", "pair dard", "haath dard"]):
        return "For bone, fracture, or joint pain, Orthopedics is suitable. You can consult Dr. Patel."

    elif has_phrase(msg, ["child", "baby", "pediatric", "bachcha", "bacha", "kids"]):
        return "For child health issues, Pediatrics is the right department. You can consult Dr. Mehta."

    elif has_phrase(msg, ["pregnancy", "period", "gynecologist", "women", "ladies doctor"]):
        return "For women’s health or pregnancy care, Gynecology is suitable. You can consult Dr. Verma."

    elif has_phrase(msg, ["doctor", "specialist", "department", "dr"]):
        return "Please tell me the health issue, like heart, skin, bone, child care, or pregnancy, and I’ll suggest the department."

    # NAVIGATION
    elif has_phrase(msg, ["mri"]):
        return "MRI room is on the 2nd floor, Block B. Take the lift near reception and turn left."

    elif has_phrase(msg, ["xray", "x-ray"]):
        return "X-ray room is on the ground floor near the lab area."

    elif has_phrase(msg, ["lab", "laboratory"]):
        return "The lab is on the ground floor near the OPD area."

    elif has_phrase(msg, ["pharmacy", "medical store", "medicine counter", "dawai"]):
        return "The pharmacy is near the main exit. Please carry your prescription."

    elif has_phrase(msg, ["icu"]):
        return "ICU is on the 3rd floor, Block C. Visitor access may be limited."

    elif has_phrase(msg, ["billing", "bill counter", "cash counter"]):
        return "Billing counter is beside the reception desk."

    elif has_phrase(msg, ["reception", "help desk", "front desk"]):
        return "Reception is at the main entrance of the hospital."

    elif has_phrase(msg, ["washroom", "toilet", "bathroom"]):
        return "Washrooms are available near the reception area and on each floor near the lift."

    elif has_phrase(msg, ["wheelchair", "patient chair"]):
        return "Wheelchair support is available near the reception. Please ask the helpdesk staff."

    elif has_phrase(msg, ["where", "kaha", "kidhar", "room", "direction", "navigate", "rasta"]):
        return "Please tell me the room or department name, like MRI, ICU, lab, pharmacy, billing, or reception."

    # BASIC SERVICES
    elif has_phrase(msg, ["upi", "cash", "card", "payment", "pay", "paisa", "paise", "online payment"]):
        return "Yes, payment support is available through UPI, cash, and card."

    elif has_phrase(msg, ["insurance", "claim", "policy", "cashless"]):
        return "For insurance or claim support, please visit the billing or insurance desk."

    elif has_phrase(msg, ["lab report", "blood report", "test result", "report", "report kaha", "report kab"]):
        return "Lab reports can be collected from the lab counter or hospital portal."

    elif has_phrase(msg, ["visiting hours", "visitor", "visit patient", "milne ka time"]):
        return "General visiting hours are 4 PM to 7 PM. ICU timings may be different."

    elif has_phrase(msg, ["hospital timing", "opening time", "closing time", "kab khulega"]):
        return "OPD is usually open from 8 AM to 10 PM. Emergency services are available 24/7."

    elif msg in ["open", "close"] or has_phrase(msg, ["hospital open", "hospital close"]):
        return "OPD is usually open from 8 AM to 10 PM. Emergency services are available 24/7."

    elif has_phrase(msg, ["parking", "car parking", "bike parking"]):
        return "Parking is available near the main entrance gate."

    elif has_phrase(msg, ["contact", "phone number", "hospital number", "call number"]):
        return "CareCircle Helpdesk: +91-9876543210"

    elif has_phrase(msg, ["blood bank", "donate blood"]):
        return "For blood bank support, please contact the emergency desk or reception."

    elif has_phrase(msg, ["oxygen", "oxygen support"]):
        return "Oxygen support is handled by emergency and critical care staff. Please contact the emergency desk immediately."

    # SYMPTOM GUIDANCE
    elif has_phrase(msg, [
        "fever", "cough", "headache", "vomiting", "stomach pain",
        "cold", "weakness", "weak", "kamjor", "kamzori",
        "thakawat", "tired", "body pain", "pet dard",
        "sir dard", "ulti", "bukhar"
    ]):
        return (
            "I can guide you to the right hospital service, but I cannot diagnose or prescribe medicine. "
            "Please consult a doctor if symptoms continue or become severe."
        )

    elif has_phrase(msg, [
        "medicine name", "which medicine", "prescribe",
        "treatment", "diagnose", "dawai batao"
    ]):
        return "I cannot prescribe medicine or diagnose illness. Please consult a qualified doctor."

    # OUT OF SCOPE
    elif has_phrase(msg, [
        "movie", "song", "game", "cricket", "instagram", "facebook",
        "shopping", "joke", "relationship", "homework", "coding", "weather"
    ]):
        return (
            "I’m sorry, I can’t help with that. "
            "I’m only made for hospital-related support like queue, appointment, doctors, rooms, billing, and emergency help."
        )

    # SIMPLE UNCLEAR QUESTIONS
    elif has_phrase(msg, ["what", "why", "how", "kaise", "kya", "kab"]):
        return (
            "Please tell me a little more clearly so I can help properly. "
            "For example: MRI room kaha hai?, token status, appointment booking, doctor suggestion, etc."
        )

    # DEFAULT
    else:
        return (
            "I didn’t understand that clearly. You can ask in simple words like:\n"
            "- MRI room kaha hai?\n"
            "- Mera token kab aayega?\n"
            "- Mujhe skin doctor chahiye\n"
            "- Appointment book karni hai\n"
            "- UPI payment hota hai?"
        )


@app.get("/")
def home():
    return {"message": "CareCircle Chatbot is running. Open /docs to test."}


@app.post("/chat")
def chat(request: ChatRequest):
    reply = chatbot_reply(request.message)
    return {"reply": reply}