import json

# ============================================================
# KNOWLEDGE BASES - 100% Offline
# ============================================================

COGNITIVE_BIASES = {
    "confirmation bias": "You only look for info that confirms what you already believe. Fix: Actively seek opposing views.",
    "sunk cost fallacy": "You keep going because of past investment not future value. Fix: Ask 'would I start this today?'",
    "dunning kruger": "The less you know the more confident you feel. Fix: Find someone better and learn from them.",
    "availability bias": "You judge likelihood by how easily examples come to mind. Fix: Look at actual statistics.",
    "negativity bias": "Bad events hit harder than good ones feel good. Fix: Consciously log 3 wins daily.",
    "spotlight effect": "You think everyone notices your mistakes. Fix: People are too busy thinking about themselves.",
    "anchoring bias": "First number you hear influences all future judgments. Fix: Always research before hearing a price.",
    "bandwagon effect": "You do things because everyone else does. Fix: Ask why YOU want it not why others have it.",
    "planning fallacy": "You underestimate time and overestimate motivation. Fix: Double your time estimate always.",
    "survivorship bias": "You only see successes not failures. Fix: Study failures as much as successes.",
}

MONEY_RULES = {
    "impulse": [
        "Wait 48 hours before any purchase over 500 rupees",
        "Ask: will this matter in 1 year?",
        "Calculate cost in work hours: price divided by hourly wage",
        "Unsubscribe from all promotional emails right now",
        "Delete saved cards from shopping apps",
    ],
    "saving": [
        "Pay yourself first: transfer savings the moment salary arrives",
        "Save minimum 20% of every income no exceptions",
        "Every raise: save 50% of the increase immediately",
        "Round up every expense and save the difference",
        "One no-spend day per week builds discipline",
    ],
    "investing": [
        "Start with index funds before individual stocks",
        "Compound interest needs time: start today not tomorrow",
        "Never invest money you need in next 3 years",
        "Invest in yourself first: skills have highest ROI",
        "Diversify: never put all money in one place",
    ],
    "mindset": [
        "Rich people buy assets. Poor people buy liabilities.",
        "Your income is the average of your 5 closest financial peers",
        "Every luxury today is a financial goal delayed",
        "Wealth is what you don't spend not what you earn",
        "Money is a tool not a goal. Freedom is the goal.",
    ],
}

DISCIPLINE_SYSTEM = {
    "morning": [
        "Wake same time every day including weekends",
        "No phone for first 30 minutes",
        "Drink water before coffee",
        "Write 3 most important tasks for today",
        "Move your body for 10 minutes minimum",
    ],
    "focus": [
        "Work in 90 minute blocks with 20 minute breaks",
        "Phone in another room during deep work",
        "One task at a time: multitasking kills quality",
        "Most important task first before email or messages",
        "Say no to everything that doesn't serve your goals",
    ],
    "habits": [
        "Attach new habit to existing one: after X I will Y",
        "Make good habits obvious and easy",
        "Make bad habits invisible and hard",
        "Never miss twice: one miss is accident two is a pattern",
        "Track your habits: what gets measured gets done",
    ],
    "evening": [
        "Review what you accomplished today",
        "Prepare tomorrow's clothes and bag tonight",
        "No screens 1 hour before sleep",
        "Write one thing you're grateful for",
        "Sleep at consistent time: sleep is performance",
    ],
}

LEARNING_METHODS = {
    "feynman": [
        "Step 1: Pick a concept you want to learn",
        "Step 2: Explain it like teaching a 10 year old",
        "Step 3: Find gaps where explanation breaks down",
        "Step 4: Go back to source and fill the gaps",
        "Step 5: Simplify further until it's crystal clear",
    ],
    "retention": [
        "Review new info after 1 day, 1 week, 1 month",
        "Teach what you learn immediately to someone",
        "Connect new info to something you already know",
        "Write by hand: typing doesn't encode as deeply",
        "Sleep after learning: brain consolidates during sleep",
    ],
    "speed": [
        "Read purpose first: what question am I answering?",
        "Skip what you already know without guilt",
        "Take breaks: 45 min study 15 min rest",
        "Eliminate subvocalization to read 3x faster",
        "Summarize each chapter in one sentence",
    ],
}

THINKING_UPGRADES = {
    "first principles": "Break any problem to its most basic truths. Ask why 5 times. Build answer from scratch.",
    "inversion": "Instead of how to succeed ask how to avoid failure. Avoid stupidity before chasing brilliance.",
    "second order": "Ask what happens after what happens. Every action has consequences of consequences.",
    "opportunity cost": "Every yes is a no to something else. What are you NOT doing by doing this?",
    "mental models": "Use frameworks from multiple fields. A biologist sees what an economist misses.",
    "via negativa": "Improve by removing not adding. What can you stop doing to become better?",
    "pareto principle": "20% of actions produce 80% of results. Find and focus on that 20%.",
    "circle of control": "Divide problems into: can control, can influence, cannot control. Focus only on first.",
}

IKIGAI_QUESTIONS = [
    "What activities make you lose track of time?",
    "What would you do even if you weren't paid?",
    "What problems in the world make you angry?",
    "What do people always ask your help with?",
    "What skills do you have that feel effortless to you?",
    "What topics do you read about without being asked?",
    "What would you regret NOT trying on your deathbed?",
    "What did you love doing as a child before money mattered?",
]

SLEEP_RULES = [
    "Consistent sleep/wake time is more important than duration",
    "Room temperature 18-19 celsius is optimal for sleep",
    "Caffeine stays in system 8 hours: no coffee after 2pm",
    "Alcohol destroys sleep quality even if it helps you fall asleep",
    "Blue light blocks melatonin: no screens 1 hour before bed",
    "Exercise improves sleep but not within 3 hours of bedtime",
    "Worry journal before bed offloads anxious thoughts",
    "Same pre-sleep routine signals brain it's time to sleep",
]

IMPULSE_QUESTIONS = [
    "Do I need this or just want it right now?",
    "How many hours of work does this cost me?",
    "Will I care about this in 6 months?",
    "Am I buying this to feel better emotionally?",
    "Do I have something that already does this job?",
]

# ============================================================
# MAIN COACHING ENGINE
# ============================================================

def get_life_coaching(topic: str, details: str = "") -> str:
    """
    Universal life coach covering mind, money, discipline,
    learning, thinking and purpose. 100% offline.
    """
    try:
        t = topic.lower().strip()
        d = details.lower().strip()
        combined = t + " " + d

        result = {}

        # ── MONEY ──────────────────────────────────────────
        if any(w in combined for w in ["money", "rich", "wealth", "saving", "invest",
                                        "spend", "salary", "broke", "debt", "budget",
                                        "impulse", "buy", "purchase", "finance"]):
            if any(w in combined for w in ["impulse", "buy", "purchase", "spend"]):
                result = {
                    "area": "💰 Money — Impulse Control",
                    "insight": "Impulse buying is emotional not logical. You buy feelings not things.",
                    "questions_to_ask_yourself": IMPULSE_QUESTIONS,
                    "rule": "48 hour rule: wait 48 hours before any non-essential purchase",
                    "truth": "Every impulse buy is stealing from your future self",
                    "action_now": "Delete one shopping app from your phone right now"
                }
            elif any(w in combined for w in ["invest", "stock", "mutual fund"]):
                result = {
                    "area": "💰 Money — Investing",
                    "rules": MONEY_RULES["investing"],
                    "truth": "Time in market beats timing the market. Start small. Start now.",
                    "action_now": "Invest even 100 rupees today to build the identity of an investor"
                }
            else:
                result = {
                    "area": "💰 Money Psychology",
                    "core_rules": MONEY_RULES["saving"],
                    "mindset_shifts": MONEY_RULES["mindset"],
                    "truth": "Wealth is built in boring consistent daily decisions not big wins",
                    "action_now": "Set up automatic transfer of 20% salary on payday"
                }

        # ── DISCIPLINE ─────────────────────────────────────
        elif any(w in combined for w in ["discipline", "habit", "routine", "lazy",
                                          "procrastinat", "motivation", "consistent",
                                          "morning", "focus", "distract", "phone"]):
            if any(w in combined for w in ["morning", "wake", "routine"]):
                result = {
                    "area": "⚡ Discipline — Morning Routine",
                    "rules": DISCIPLINE_SYSTEM["morning"],
                    "truth": "Win the morning and you win the day. Lose it and you spend all day catching up.",
                    "action_now": "Set tomorrow's wake time right now. Same as today but 30 min earlier."
                }
            elif any(w in combined for w in ["focus", "distract", "phone", "social media"]):
                result = {
                    "area": "⚡ Discipline — Deep Focus",
                    "rules": DISCIPLINE_SYSTEM["focus"],
                    "truth": "Every notification is someone else's priority interrupting yours",
                    "action_now": "Turn on Do Not Disturb for next 90 minutes and do one important task"
                }
            else:
                result = {
                    "area": "⚡ Discipline System",
                    "habit_rules": DISCIPLINE_SYSTEM["habits"],
                    "evening_rules": DISCIPLINE_SYSTEM["evening"],
                    "truth": "Motivation is a myth. Systems beat willpower every single time.",
                    "action_now": "Pick ONE habit. Attach it to something you already do daily."
                }

        # ── THINKING ───────────────────────────────────────
        elif any(w in combined for w in ["think", "smart", "decision", "problem",
                                          "bias", "logic", "reason", "choice", "stuck"]):
            if any(w in combined for w in ["bias", "logical", "fallacy"]):
                detected = []
                for bias, explanation in COGNITIVE_BIASES.items():
                    if any(word in combined for word in bias.split()):
                        detected.append({"bias": bias, "explanation": explanation})
                result = {
                    "area": "🧠 Thinking — Bias Awareness",
                    "detected_biases": detected if detected else list(COGNITIVE_BIASES.items())[:3],
                    "truth": "You cannot think your way out of a bias you cannot see",
                    "action_now": "Before next big decision write down 3 ways you could be wrong"
                }
            else:
                upgrades = list(THINKING_UPGRADES.items())[:4]
                result = {
                    "area": "🧠 Thinking Upgrades",
                    "mental_models": [
                        {"model": k, "how_to_use": v} for k, v in upgrades
                    ],
                    "truth": "Most people react. Smart people think in systems and models.",
                    "action_now": "Apply inversion to your biggest current problem right now"
                }

        # ── LEARNING ───────────────────────────────────────
        elif any(w in combined for w in ["learn", "study", "memory", "read", "skill",
                                          "understand", "forget", "exam", "course"]):
            result = {
                "area": "📚 Learning — Feynman Method",
                "steps": LEARNING_METHODS["feynman"],
                "retention_hacks": LEARNING_METHODS["retention"],
                "truth": "If you cannot explain it simply you do not understand it yet",
                "action_now": "Take the last thing you learned and explain it out loud right now"
            }

        # ── PURPOSE / IKIGAI ───────────────────────────────
        elif any(w in combined for w in ["purpose", "ikigai", "direction", "career",
                                          "passion", "meaning", "lost", "goal", "life"]):
            result = {
                "area": "🎯 Purpose — Ikigai Discovery",
                "reflect_on_these": IKIGAI_QUESTIONS,
                "truth": "Most people never find purpose because they wait to feel it instead of doing things until they find it",
                "framework": {
                    "love": "What you love",
                    "good_at": "What you are good at",
                    "world_needs": "What the world needs",
                    "paid_for": "What you can be paid for",
                    "ikigai": "Where all 4 overlap — that is your reason for being"
                },
                "action_now": "Answer question 1 and 5 from the list above right now in writing"
            }

        # ── SLEEP / HEALTH ─────────────────────────────────
        elif any(w in combined for w in ["sleep", "tired", "energy", "health",
                                          "rest", "fatigue", "wake up", "insomnia"]):
            result = {
                "area": "😴 Health — Sleep Optimization",
                "rules": SLEEP_RULES,
                "truth": "Sleep is not rest. Sleep is performance. Every hour lost costs 3 hours of productivity.",
                "action_now": "Set a fixed sleep time tonight and stick to it for 7 days straight"
            }

        # ── DEFAULT — DAILY UPGRADE ────────────────────────
        else:
            result = {
                "area": "🚀 Daily Human Upgrade",
                "thinking": list(THINKING_UPGRADES.items())[0],
                "money": MONEY_RULES["mindset"][0],
                "discipline": DISCIPLINE_SYSTEM["habits"][0],
                "learning": LEARNING_METHODS["feynman"][0],
                "sleep": SLEEP_RULES[0],
                "truth": "Small daily improvements compound into massive life changes",
                "action_now": "What is the ONE thing you can do today that makes everything else easier?",
                "available_topics": [
                    "money", "discipline", "thinking",
                    "learning", "purpose", "sleep", "habits"
                ]
            }

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


# ============================================================
# TEST
# ============================================================
if __name__ == "__main__":
    tests = ["money", "discipline", "thinking bias",
             "learning", "purpose", "sleep", "impulse buying"]
    for t in tests:
        r = json.loads(get_life_coaching(t))
        print(f"\n✅ {r.get('area','?')}")
        print(f"   → {r.get('action_now','?')}")