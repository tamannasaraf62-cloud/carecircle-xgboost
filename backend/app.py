from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CareCircle Chatbot")


class ChatRequest(BaseModel):
    message: str


def chatbot_reply(message: str):

    msg = message.lower().strip()

    # EMPTY MESSAGE
    if msg == "":
        return (
            "Please type your question. "
            "I can help with emergency, queue status, appointments, "
            "doctor information, billing, lab reports, and hospital navigation."
        )

    # GREETING
    elif any(word in msg for word in ["hi", "hello", "hey", "good morning", "good evening"]):
        return (
            "Hello! I am CareCircle Assistant. "
            "How can I help you today?"
        )

        # EMERGENCY PRIORITY SYSTEM

    elif any(word in msg for word in [
        "heart attack",
        "chest pain",
        "stroke",
        "seizure",
        "unconscious",
        "can't breathe",
        "not breathing"
    ]):
        return (
            "🚨 Priority Level: CRITICAL\n"
            "This may be a life-threatening emergency.\n"
            "Please go to the emergency ward immediately or call an ambulance."
        )

    elif any(word in msg for word in [
        "breathing problem",
        "asthma attack",
        "accident",
        "heavy bleeding",
        "severe pain"
    ]):
        return (
            "🚑 Priority Level: HIGH\n"
            "Urgent medical attention may be required.\n"
            "Please inform hospital staff immediately."
        )
        return (
            "🚨 Emergency detected. "
            "Please go to the emergency ward immediately or call an ambulance."
        )

    # AMBULANCE
    elif any(word in msg for word in ["ambulance", "emergency vehicle"]):
        return (
            "🚑 Ambulance support requested. "
            "Please share your location or contact hospital emergency desk immediately."
        )

        # TOKEN GENERATION

    elif any(word in msg for word in [
        "generate token",
        "new token",
        "assign token",
        "give token"
    ]):
        return (
            "🎫 Token Generated Successfully\n"
            "Patient Token: CC-019\n"
            "Department: General OPD\n"
            "Estimated Wait Time: 20 minutes\n"
            "Please keep this token for queue tracking."
        )
       # SMART QUEUE STATUS

    elif any(word in msg for word in [
        "queue",
        "wait",
        "waiting",
        "token",
        "turn",
        "doctor late",
        "doctor delay"
    ]):
        current_token = 15
        your_token = 19
        avg_time_per_patient = 5
        patients_before_you = your_token - current_token
        estimated_wait = patients_before_you * avg_time_per_patient

        return (
            f"⏳ Queue Status\n"
            f"Current Token: {current_token}\n"
            f"Your Token: {your_token}\n"
            f"Patients Before You: {patients_before_you}\n"
            f"Estimated Waiting Time: {estimated_wait} minutes\n"
            f"Note: Waiting time may change if emergency cases arrive."
        )

        # PATIENT REGISTRATION

    elif any(word in msg for word in [
        "register patient",
        "patient registration",
        "new patient",
        "registration"
    ]):
        return (
            "📝 Patient Registration Support\n"
            "Please provide:\n"
            "1. Patient Name\n"
            "2. Age\n"
            "3. Gender\n"
            "4. Mobile Number\n"
            "5. Main Health Concern\n\n"
            "After registration, CareCircle can assign a token number."
        )
    
    
    
        # APPOINTMENT BOOKING DEMO

    elif any(word in msg for word in [
        "appointment",
        "book",
        "cancel",
        "reschedule",
        "schedule"
    ]):
        return (
            "📅 Appointment Support\n"
            "Available Demo Slots:\n"
            "1. Cardiology - Dr. Sharma - 10:00 AM\n"
            "2. Dermatology - Dr. Khan - 12:30 PM\n"
            "3. Orthopedics - Dr. Patel - 3:00 PM\n\n"
            "To book, please provide:\n"
            "Doctor name, date, and preferred time."
        )
       # HOSPITAL NAVIGATION

    elif "mri" in msg:
        return (
            "🧭 MRI Room is located on 2nd Floor, Block B. "
            "Take the lift near Reception and turn left."
        )

    elif "lab" in msg:
        return (
            "🧪 Laboratory is on Ground Floor near OPD section."
        )

    elif "pharmacy" in msg:
        return (
            "💊 Pharmacy is near the hospital main exit."
        )

    elif "icu" in msg:
        return (
            "🏥 ICU is located in Block C, 3rd Floor. "
            "Visitor access may be restricted."
        )

    elif "billing" in msg:
        return (
            "💳 Billing Counter is beside Reception Desk."
        )

    elif any(word in msg for word in [
        "room",
        "direction",
        "where",
        "navigate"
    ]):
        return (
            "🧭 Please tell me the department or room name "
            "for navigation assistance."
        )
         # SMART DOCTOR RECOMMENDATION

    elif any(word in msg for word in ["heart", "chest", "cardio", "cardiologist"]):
        return (
            "👨‍⚕️ Recommended Department: Cardiology\n"
            "Suggested Doctor: Dr. Sharma\n"
            "Reason: Heart/chest-related symptoms need cardiac evaluation."
        )

    elif any(word in msg for word in ["skin", "rash", "itching", "dermatologist"]):
        return (
            "👩‍⚕️ Recommended Department: Dermatology\n"
            "Suggested Doctor: Dr. Khan\n"
            "Reason: Skin-related symptoms should be checked by a dermatologist."
        )

    elif any(word in msg for word in ["bone", "fracture", "joint pain", "orthopedic"]):
        return (
            "👨‍⚕️ Recommended Department: Orthopedics\n"
            "Suggested Doctor: Dr. Patel\n"
            "Reason: Bone, fracture, and joint issues need orthopedic care."
        )

    elif any(word in msg for word in ["child", "baby", "pediatric", "pediatrician"]):
        return (
            "👩‍⚕️ Recommended Department: Pediatrics\n"
            "Suggested Doctor: Dr. Mehta\n"
            "Reason: Child and baby health issues need pediatric care."
        )

    elif any(word in msg for word in ["pregnancy", "period", "gynecologist", "women"]):
        return (
            "👩‍⚕️ Recommended Department: Gynecology\n"
            "Suggested Doctor: Dr. Verma\n"
            "Reason: Women’s health and pregnancy care need gynecology support."
        )

    elif any(word in msg for word in ["doctor", "specialist"]):
        return (
            "Please tell me your symptom or department, such as heart, skin, bone, child, or pregnancy care."
        )

    # SYMPTOMS
    elif any(word in msg for word in [
        "fever",
        "cough",
        "headache",
        "vomiting",
        "stomach pain",
        "cold",
        "body pain",
        "dizziness",
        "weakness"
    ]):
        return (
            "I can provide basic hospital guidance, "
            "but I cannot diagnose disease or prescribe medicine. "
            "Please consult a doctor."
        )

    # MEDICINE
    elif any(word in msg for word in [
        "medicine",
        "tablet",
        "pharmacy medicine",
        "drug"
    ]):
        return (
            "Please visit the pharmacy counter for medicine availability and prescription support."
        )

    # LAB REPORTS
    elif any(word in msg for word in [
        "lab report",
        "blood report",
        "test result",
        "report collection"
    ]):
        return (
            "Lab reports can be collected from the laboratory department "
            "or hospital portal."
        )

    # BILLING
    elif any(word in msg for word in [
        "payment",
        "upi",
        "cash",
        "card",
        "bill",
        "billing"
    ]):
        return (
            "We support UPI, cash, card, and insurance-related billing assistance."
        )

    # INSURANCE
    elif any(word in msg for word in [
        "insurance",
        "claim",
        "policy"
    ]):
        return (
            "Please contact the insurance or billing desk "
            "for claim processing and policy verification."
        )

    # VISITING HOURS
    elif any(word in msg for word in [
        "visiting hours",
        "visitor timing",
        "visit patient"
    ]):
        return (
            "General visiting hours are from 4 PM to 7 PM. "
            "ICU visiting hours may vary."
        )

    # CHILD EMERGENCY
    elif any(word in msg for word in [
        "baby fever",
        "child emergency",
        "child not breathing"
    ]):
        return (
            "🚨 Pediatric emergency detected. "
            "Please contact emergency services immediately."
        )

    # CONDITION WORSENING
    elif any(word in msg for word in [
        "condition worsening",
        "patient serious",
        "can't breathe"
    ]):
        return (
            "🚨 Your condition may require urgent medical attention. "
            "Please inform nearby hospital staff immediately."
        )

    # THANK YOU
    elif any(word in msg for word in [
        "thanks",
        "thank you",
        "bye",
        "ok",
        "okay"
    ]):
        return (
            "Thank you for using CareCircle Assistant. "
            "Take care and stay safe."
        )

        # INVALID / OUT OF SCOPE QUESTIONS

    elif any(word in msg for word in [
        "movie",
        "song",
        "game",
        "cricket",
        "instagram",
        "facebook",
        "shopping",
        "weather",
        "politics",
        "joke",
        "relationship",
        "homework",
        "coding"
    ]):
        return (
            "❌ This feature is not available in CareCircle Assistant.\n\n"
            "I can only help with:\n"
            "🚨 Emergency support\n"
            "⏳ Queue status\n"
            "📅 Appointments\n"
            "🧭 Hospital navigation\n"
            "👨‍⚕️ Doctor recommendation\n"
            "💳 Billing and insurance\n"
            "🧪 Lab reports"
        )

        # HOSPITAL SERVICE MENU

    elif any(word in msg for word in [
        "menu",
        "services",
        "help",
        "what can you do"
    ]):
        return (
            "🏥 CareCircle Services\n"
            "1. 🚨 Emergency priority detection\n"
            "2. 🎫 Patient registration and token support\n"
            "3. ⏳ Queue status tracking\n"
            "4. 📅 Appointment support\n"
            "5. 👨‍⚕️ Doctor recommendation\n"
            "6. 🧭 Hospital navigation\n"
            "7. 💳 Billing and insurance help\n"
            "8. 🧪 Lab report support\n"
            "9. 💊 Pharmacy guidance\n\n"
            "Please ask any hospital-related question."
        )
    
        # MEDICAL SAFETY DISCLAIMER

    elif any(word in msg for word in [
        "can you diagnose",
        "give medicine",
        "which medicine",
        "prescribe",
        "treatment"
    ]):
        return (
            "⚠️ Medical Safety Notice\n"
            "CareCircle Assistant cannot diagnose disease, prescribe medicine, "
            "or replace a doctor. Please consult qualified medical staff."
        )
    
    elif any(word in msg for word in [
        "hospital timing",
        "opening time",
        "closing time",
        "open hospital"
    ]):
        return (
            "🏥 Hospital Timings:\n"
            "Monday - Saturday: 8 AM to 10 PM\n"
            "Emergency services are available 24/7."
        )

    elif any(word in msg for word in [
        "parking",
        "car parking",
        "bike parking"
    ]):
        return (
            "🚗 Parking Area is available near the main entrance gate."
        )
    
    elif any(word in msg for word in [
        "contact",
        "phone number",
        "hospital number"
    ]):
        return (
            "☎️ CareCircle Helpdesk:\n"
            "+91-9876543210\n"
            "carecircle.support@gmail.com"
        )
    
    elif any(word in msg for word in [
        "emergency number",
        "ambulance number"
    ]):
        return (
            "🚑 Emergency Helpline:\n"
            "102 / 108"
        )
    # DEFAULT RESPONSE
    else:
        return (
            "Sorry, I could not understand your request. "
            "Please ask about emergency help, appointments, queue status, "
            "hospital navigation, doctor information, billing, or lab reports."
        )


@app.get("/")
def home():
    return {
        "message": "CareCircle Chatbot is running. Open /docs to test."
    }


@app.post("/chat")
def chat(request: ChatRequest):

    reply = chatbot_reply(request.message)

    return {
        "reply": reply
    }