from .models import Alert

def calculate_risk(student, wellbeing):

    score = 0

    reasons = []

    recommendations = []


    if student.attendance < 75:

        score += 12.5

        reasons.append(
            "Low attendance"
        )


    if student.marks < 60:

        score += 12.5

        reasons.append(
            "Poor academic performance"
        )


    if student.discipline < 60:

        score += 12.5

        reasons.append(
            "Discipline concerns"
        )


    if wellbeing.stress_level >= 7:

        score += 12.5

        reasons.append(
            "High stress level"
        )


    if wellbeing.sleep_quality <= 4:

        score += 12.5

        reasons.append(
            "Poor sleep quality"
        )



    if wellbeing.social_activity <= 4:

        score += 12.5

        reasons.append(
            "Low social interaction"
        )

    if wellbeing.motivation_level <= 4:

        score += 12.5

        reasons.append(
            "Low motivation"
        )


    if wellbeing.mood in ['Sad', 'Anxious']:

        score += 12.5

        reasons.append(
            "Negative emotional wellbeing"
        )

    if score <= 35:

        risk = 'Low'

        recommendations.append(
            'Student is stable'
        )

    elif score <= 65:

        risk = 'Medium'

        recommendations.append(
            'Needs monitoring and counselling'
        )

    else:

        risk = 'High'

        recommendations.append(
            'Immediate intervention required'
        )

    student.risk_level = risk

    student.risk_score = score

    student.risk_reason = ", ".join(
        reasons
    )

    student.ai_recommendation = ", ".join(
        recommendations
    )

    student.save()


    if risk in ['Medium', 'High']:

        Alert.objects.create(

            student=student,

            risk_level=risk,

            risk_score=score,

            message=student.risk_reason
        )

    return risk  