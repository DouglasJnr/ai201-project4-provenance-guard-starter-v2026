"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "My name is Douglas Tanyanyiwa, and I'm an international student from Zimbabwe. I'm an honors computer science major who will be graduating in December. My goal is to become an AI engineer at one of the FAANG companies. I've dreamed of this since I was a child",
            "If there's anything I love in life, it's God. He has been faithful. I was raised in a Christian household so He's been all I know. Until He wasn't. Life showed me different options. I have veered off multiple times. I have tried to be my own hero. But through it all, He calls me back. I'm proud to say, I'm a Christian",
            "Sometimes I wonder if there's more to life. Not in a doom and gloom kind of way, but plain curiosity. What else could be out there? What are we yet to discover? How much do we truly know? Questions I usually sit and ponder. Life is beautiful, but I often qestion how much is yet to be discovered.",
            "If I could write you a song to make you fall in love, I would already have you right under my arms. Writing has always been my outlet. But somehow when it comes to you, I get stumped. A heart full of emotions but empty pages stare back at me. Nothing. Absolutely nothing! I guess this is what they call being left speechless.",
            "I didn't sleep. Not properly, anyway — I lay there listening to the boiler tick and thinking about the thing I'd said to Marcus at the pub, which was stupid, and which he will absolutely bring up again. Twice now. So: coffee, and the long way round to work, and a plan. The plan lasted until about ten past nine, when Priya asked how the weekend was and I said \"fine\" in the voice that means it wasn't, and she put her mug down and looked at me. That's the trouble with Priya. She notices.",
            "Sometimes being overseas is fun. But more often than not I miss home. How could I not? My whole childhood was there. Who I am today is because of it. Family, friends, memories, the culture, the food, the list is endless. And here I am a foreigner. Nothing I'm used to. Everyone and everything is different, but somehow I have to find a middle ground. Honestly, sometimes I don't see it, and sometimes I don't want to see it. But every day the sun rises and I try again.",
            "My greatest investment to this day has been my MacBook, and convincing my mother to get it at today’s prices was indisputably a top three achievement. Through my Udemy courses I have made a few projects; my favorite was an interactive birthday webpage for my church apostle (due to the smile on her face when she saw it). However, coding simple webpages isn’t where I intend to stop.",
            "My goal is to, as former Navy Seal, public speaker, and author David Goggins says, “Be uncommon amongst uncommon people.” My inquisitive nature has always driven me to seek knowledge beyond the confines of the classroom. The University of Miami's distinguished faculty members, luminaries in their fields, beckon with the promise of not just teaching but guiding—mentorship that extends beyond textbooks and exams. It's a symbiotic relationship, a dance between seeker and sage, where intellectual curiosity is not merely satisfied but ignited afresh with each shared insight.",
            "The University of Miami emerges as the perfect nexus for my inquisitive, adventurous, and hardworking nature. My journey at UM will not be a solitary expedition but a shared odyssey; an exploration of knowledge and a celebration of diversity. Computer Science is not just logic and code. It is the culmination of artistic expression and a reflection of my commitment to technology as a quality of freedom and empowerment.",
            "As the sun casts its golden hues over a landscape adorned with dew-kissed grass and gently swaying palm trees, a soft breeze carries the sweet scent of blossoms, and the air hums with the melodies of chirping birds. It's the kind of morning that whispers promises of leisure and rejuvenation, a moment frozen in time where the world seems to exhale in collective contentment. Yet, in the Tanyanyiwa household, this idyllic scene of peace and serenity is the calm before the storm.",
        ],
    },
    {
        "name": "score spread",
        "criterion": 2,
        "texts": [
            "As the sun casts its golden hues over a landscape adorned with dew-kissed grass and gently swaying palm trees, a soft breeze carries the sweet scent of blossoms, and the air hums with the melodies of chirping birds. It's the kind of morning that whispers promises of leisure and rejuvenation, a moment frozen in time where the world seems to exhale in collective contentment. Yet, in the Tanyanyiwa household, this idyllic scene of peace and serenity is the calm before the storm.",
            "An hour until kick-off, the announcement of the team line-ups saw the round table of the “football (soccer) experts” converge in the living room—united by passion for the game. In this gathering, due diligence was ensured. The score lines were predicted, the coach’s thought process was analyzed and evaluated, line-ups were dissected to the finest detail, and family bonds were strengthened.",
            "A rookie mistake. My heart stopped as the massive yellow triangle glared at me with an exclamation point inside—I had bricked my brand-new Samsung Galaxy S4! I held my composure and researched my way to a fix before my mom found out. I didn’t let that stop me as I continued my quest to root my phone, which was successful at the second time of asking. This was the first of many more successful attempts with every new phone I got—to spice things up I moved to jailbreaking once I switched over to using iPhones.",
            "It was not my technical prowess that I got noticed for, or that earned me access to some of the distinguished guests I spoke to. It was perception. It was the ability to articulate my technical knowledge that led to people viewing me as brilliant. It was not in the class that I developed the skills that aided me in that moment, but outside. My social and interpersonal communication skills were garnered through being captain on sports teams or allied arts (speech and drama festival) competitions during my primary school years.",
            "My home away from home—Fellowship for Christian Athletes (FCA). My relationship with God is my most prized possession, nurtured through prayer, bible study, serving in church and fellowshipping with other Christians. Having moved across the world, I lost the last two which helped strengthen the first two. FCA has not only helped me maintain my relationship but provides an escape and comfort from the stresses of being an international student in college.",
            "Effective time management is an essential skill for personal and professional development. First, establishing clear priorities allows individuals to focus their energy on the most important responsibilities. Additionally, creating a structured schedule helps reduce procrastination and improves overall productivity. Moreover, breaking larger tasks into smaller, manageable steps can significantly reduce feelings of stress and overwhelm. It is also important to recognize the value of regular breaks, which support sustained concentration and mental wellbeing. Furthermore, leveraging digital tools such as calendars and task management applications can enhance organization and accountability. Ultimately, effective time management is not about doing more, but about doing what matters most. By implementing these strategies consistently, individuals can achieve a healthier balance and greater long-term success.",
            "Climate change represents one of the most significant challenges facing the modern world. Rising global temperatures are contributing to more frequent and severe weather events across many regions. Additionally, melting polar ice is accelerating sea level rise, which threatens coastal communities and ecosystems. Furthermore, shifts in precipitation patterns are affecting agricultural productivity and global food security. However, there are meaningful opportunities for positive change through innovation and collaboration. Renewable energy technologies, such as solar and wind power, are becoming increasingly accessible and affordable. Moreover, international agreements encourage nations to reduce emissions and pursue sustainable development. Ultimately, addressing climate change requires coordinated action from governments, businesses, and individuals. By working together, society can build a more resilient and sustainable future for generations to come.",
            "Artificial intelligence is transforming the way organizations operate across a wide range of industries. In healthcare, intelligent systems are improving diagnostic accuracy and supporting personalized treatment recommendations. Additionally, in the financial sector, machine learning algorithms enhance fraud detection and risk management. Furthermore, customer service has benefited from conversational assistants that provide immediate and consistent support. However, the widespread adoption of artificial intelligence also raises important ethical considerations. Issues such as data privacy, algorithmic bias, and transparency require careful attention and thoughtful regulation. Moreover, organizations must invest in workforce development to ensure employees can adapt to evolving responsibilities. Ultimately, the successful implementation of artificial intelligence depends on balancing innovation with accountability. By prioritizing responsible development, organizations can unlock significant value while maintaining public trust.",
            "Regular physical activity plays a crucial role in maintaining overall health and wellbeing. First, consistent exercise strengthens the cardiovascular system and reduces the risk of chronic disease. Additionally, physical activity supports healthy weight management and improves metabolic function. Moreover, exercise has a significant positive impact on mental health by reducing symptoms of anxiety and depression. It also contributes to better sleep quality, which further enhances cognitive performance and emotional stability. Furthermore, engaging in group activities can foster social connection and a sense of community. Importantly, individuals do not need intense routines to experience these benefits, as moderate activity is often sufficient. Ultimately, incorporating movement into daily life is a practical and effective investment. By making exercise a consistent habit, individuals can significantly improve their quality of life.",
            "Effective communication is a fundamental component of successful teamwork in any organization. First, clear communication ensures that team members understand their responsibilities and shared objectives. Additionally, open dialogue encourages collaboration and allows diverse perspectives to contribute to better decision-making. Moreover, active listening fosters mutual respect and helps prevent misunderstandings before they escalate into conflict. It is also important to provide constructive feedback in a timely and respectful manner. Furthermore, leveraging appropriate communication tools can enhance coordination, particularly within remote or distributed teams. Consequently, organizations that prioritize communication often experience higher engagement and improved performance. Ultimately, strong communication creates an environment of trust and accountability. By investing in these skills, teams can navigate challenges more effectively and achieve their goals with greater consistency.",
            ]
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Inputs spread across your score range, so you can check all three
        # labels are actually reachable.
        "texts": [
            # clearly human
            "I didn't sleep. Not properly, anyway — I lay there listening to the boiler tick and thinking about the thing I'd said to Marcus at the pub, which was stupid, and which he will absolutely bring up again. Twice now. So: coffee, and the long way round to work, and a plan. The plan lasted until about ten past nine, when Priya asked how the weekend was and I said \"fine\" in the voice that means it wasn't, and she put her mug down and looked at me. That's the trouble with Priya. She notices.",
            " I initially began as the introverted and reserved version of myself, but I have grown into an ambivert. Often bringing others to participate, or leading bible study and discussions weekly. FCA has provided me the joy, comfort, and relief, I felt when I prayed and studied my bible in, and satisfaction and purpose when I served and fellowshipped back home.",
            "Football has been one of the biggest aspects of my life growing up, stemming from these moments we shared as a family. Today, years after that tradition began, it holds strong even after the passing of our father in 2018, and all four of us being scattered across 4 different time zones in the US. We have never supported the same teams and never will. While we may not watch matches together, the banter that follows seeing the other’s team lose is a bond that we cherish and can never be broken.",
            "My heart was still racing. I, an alumnus, had just stood before the first lady of Zimbabwe and five members of parliament, shared about my experience and what I gained from it, all while encouraging the current crop. But somehow standing before such prominent people wasn’t the highlight of that experience. It was the aftermath of receiving praises that stood out, and where I learned my biggest lesson---perception is everything.",
            "For the next month I found myself attending church not just as a member of the congregation, but as a servant (something I never thought I would do). I was born in a Christian home, which meant I was always in and around church. However, I was not the most committed individual in going to church. I much preferred focusing on my academics, soccer, and basketball: things I was good at and loved doing. ",
            # clearly AI
            "The importance of effective time management cannot be overstated in today's fast-paced work environment. Professionals who develop strong organizational habits are better positioned to meet deadlines and reduce stress. There are several key strategies that can help individuals improve their productivity. First, prioritization is essential. By identifying the most important tasks and addressing them first, workers can ensure that critical objectives are met. Second, minimizing distractions plays a significant role. Setting aside dedicated blocks of time for concentrated work is widely considered beneficial. Finally, regular breaks are important for maintaining performance.",
            "Remote work has fundamentally reshaped the modern workplace in recent years. First, it offers employees greater flexibility and autonomy over their daily schedules. Additionally, organizations benefit from access to a broader and more diverse talent pool. Moreover, reduced commuting time can contribute to improved wellbeing and productivity. However, remote work also presents notable challenges, including communication barriers and feelings of isolation. Therefore, organizations must implement effective collaboration tools and establish clear expectations. Furthermore, regular virtual check-ins can help maintain engagement and a sense of connection. Ultimately, the success of remote work depends on thoughtful implementation and ongoing adaptation. By balancing flexibility with structure, organizations can create sustainable and productive remote environments.",
            "Financial literacy is an essential foundation for long-term stability and independence. First, understanding how to create and maintain a budget enables individuals to manage their resources effectively. Additionally, knowledge of saving and investing helps people build wealth and prepare for future goals. Moreover, awareness of credit management can prevent costly debt and improve financial opportunities. Importantly, financial education empowers individuals to make informed decisions in an increasingly complex economy. Furthermore, schools and communities play a significant role in promoting these valuable skills. Consequently, individuals with strong financial literacy often experience reduced stress and greater confidence. Ultimately, investing in financial education benefits both individuals and society as a whole.",
            "Reading offers numerous benefits that extend far beyond simple entertainment. First, regular reading strengthens vocabulary, comprehension, and critical thinking skills. Additionally, engaging with diverse perspectives fosters empathy and a deeper understanding of others. Moreover, reading has been shown to reduce stress and promote relaxation. Furthermore, it supports cognitive health by keeping the mind active and engaged throughout life. Importantly, reading also encourages creativity and imagination by exposing individuals to new ideas. Consequently, people who read consistently often demonstrate improved communication and analytical abilities. Ultimately, cultivating a reading habit is a valuable investment in personal growth. By setting aside time each day, individuals can experience these meaningful benefits.",
            "Sustainable urban planning is essential for creating livable and resilient cities. First, efficient public transportation systems reduce traffic congestion and lower carbon emissions. Additionally, the integration of green spaces enhances air quality and supports community wellbeing. Moreover, mixed-use development encourages walkability and strengthens local economies. Furthermore, sustainable infrastructure, such as energy-efficient buildings, contributes to long-term environmental goals. However, successful implementation requires collaboration between governments, developers, and residents. Therefore, inclusive planning processes are critical to ensuring that diverse community needs are addressed. Ultimately, sustainable urban planning balances economic growth with environmental responsibility. By prioritizing these principles, cities can thrive while protecting resources for future generations.",
            # borderline
            "Learning a second language as an adult is hard, but it's more doable than most people think. The biggest factor is consistency. Twenty minutes a day beats a three-hour session once a week, because memory works through repetition. Apps help, though they tend to plateau after the basics. Real conversation is where progress actually happens. I'd also say don't be afraid of sounding silly. Native speakers are usually patient, and mistakes are how you learn what sounds natural.",
            "The quarterly review highlighted several areas for improvement within the support team. Response times increased by roughly twelve percent compared with the previous quarter, largely due to staffing shortages in March. Customer satisfaction scores remained stable overall. However, feedback indicated frustration with repeated transfers between departments. The team proposes a single point of contact for escalated tickets. This change should reduce handoffs and improve accountability. We will revisit the results at the next review.",
            "Cooking at home has a lot going for it. It's usually cheaper than eating out, and you know exactly what goes into your food. It doesn't have to be complicated, either. A handful of reliable recipes covers most weeknights. Batch cooking on Sundays saves a surprising amount of time. The main obstacle is energy, honestly — after a long day, ordering in is tempting. Keeping simple ingredients on hand makes it easier to resist.",
            "Time management matters more than people admit, especially now that work moves as fast as it does. If you're organised you hit deadlines, and you're less frazzled doing it. A few things actually help. Prioritise — work out what genuinely matters and do that first. Cut the interruptions; notifications wreck focus and the damage is worse than it feels at the time. And take breaks, short ones, often.",
            "Social media has changed how people get their news. Information spreads faster than ever, which is useful during emergencies. On the other hand, misinformation spreads just as quickly, and corrections rarely travel as far. Algorithms tend to show people content they already agree with. That makes it harder to encounter different viewpoints. Checking sources takes effort, but it's worth it. A good habit is to pause before sharing anything that provokes a strong reaction.",
        ],
    },
    # Criterion 4 (appeal path) isn't here: it needs a real content_id from
    # /submit and then a POST to /appeal, which run_eval.py doesn't do. It's
    # tested by run_appeals.py instead.
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
        {"text": "", "creator_id": "eval_bad_empty"},
        {"creator_id": "eval_bad_missing"},          # no text field at all
        {"text": "word " * 20000, "creator_id": "eval_bad_huge"},
        {"text": None, "creator_id": "eval_bad_null"},
        {"text": "   \n\t  ", "creator_id": "eval_bad_whitespace"},
        {"text": 12345, "creator_id": "eval_bad_nonstring"},
        {"text": "I walked to the shop this morning and it was raining, so I came back soaked and in a bad mood.", "creator_id": "eval_bad_short"},
        ],
    },

    # TODO: add what your remaining criteria need.
    #
    # A criterion about the appeal path can't be tested by sending text alone;
    # it needs a submission first and then an appeal against the content_id
    # that came back. You'll need to test that one by hand, or extend this file
    # and run_eval.py to do it. Saying which you did is part of the write-up.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
