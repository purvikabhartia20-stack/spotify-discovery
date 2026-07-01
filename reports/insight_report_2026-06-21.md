# Spotify Discovery Insights Report
*Generated on 2026-06-21*

## Conclusion

### Executive Summary

Spotify's ability to facilitate music discovery is currently severely undermined by a degraded foundational user experience and a significant erosion of trust, rather than solely by shortcomings in its recommendation algorithms. Users are fundamentally frustrated by excessive ads, restrictive paywalls that impede basic listening control, and a perception that the platform increasingly prioritizes monetization over user value. Compounding this, a lack of trust in content authenticity (e.g., AI music) and insufficient tools to control or provide negative feedback on recommendations further disincentivize exploration. This collective friction leads users to stick with familiar content, disengage from discovery features, and ultimately question the overall value proposition of Spotify.

### Top 3 Unmet Needs

1.  **Uninterrupted & Controllable Core Listening Experience:** Users desperately need to listen to music without constant interruptions from excessive ads or arbitrary paywalls that restrict basic playback actions like picking specific songs, skipping, or looping, particularly within the free tier.
2.  **Empowered & Trustworthy Personalization:** Users desire highly relevant music recommendations, coupled with clear, explicit tools to filter out unwanted content (e.g., specific artists, genres, or AI-generated music) and provide effective negative feedback, thereby fostering trust in the content and a sense of agency over their listening journey.
3.  **Clear Value & Reliable Platform Performance:** Users expect a fair and consistent value exchange for their time or money, free from unexpected feature removals, aggressive price increases, and fundamental app stability issues (crashes, lag) that hinder their ability to use Spotify effectively for any purpose, including discovery.

### Recommended Next Steps

1.  **Experiment: "Free Tier Discovery Refresh"**
    *   **Goal:** Re-engage free users with discovery by offering more controlled flexibility, thereby creating a more positive path to premium conversion.
    *   **Description:** A/B test a modified free-tier experience where users receive a limited number of "Discovery Tokens" daily. These tokens could allow them to explicitly pick a song from a recommended discovery playlist (e.g., Daily Mix), skip an unwanted track from a personalized radio station without penalty, or unlock a short ad-free discovery session.
    *   **Metrics:** Track engagement with discovery features, daily active users, retention rates of the new free tier, and conversion to premium subscribers compared to the current free tier.

2.  **Experiment: "Negative Feedback & Content Filter"**
    *   **Goal:** Empower users with greater control over their recommendations and address concerns about content authenticity.
    *   **Description:** Implement and A/B test a more prominent and effective "Dislike Artist/Band" or "Block Content Type" feature, accessible directly during playback and within recommendation feeds. Crucially, include an explicit option for users to filter out or report "AI-generated music" if detected. This feedback should visibly influence subsequent recommendations.
    *   **Metrics:** Measure adoption rates of the new feedback options, user satisfaction scores for recommendation quality, and a reduction in negative sentiment related to unwanted content (e.g., AI music) in feedback channels.

3.  **Experiment: "Core Experience Stability Sprint & Communication"**
    *   **Goal:** Rebuild trust and improve overall platform reliability, making users more willing to engage with any feature, including discovery.
    *   **Description:** Dedicate a focused engineering sprint (e.g., 4-6 weeks) to address the top 3-5 most severe app stability issues (e.g., frequent crashes, slow loading times, unresponsive controls) identified in recent user reviews. Concurrently, launch a transparent in-app message or short blog post titled "We're Listening: Improving Your Core Spotify Experience," detailing the specific issues addressed and Spotify's commitment to foundational quality.
    *   **Metrics:** Monitor changes in app store ratings, crash rates, load times, and overall sentiment in user feedback channels following the release and communication efforts.

---

## 1. Why do users struggle to discover new music?

**The primary impediment to new music discovery stems from a fundamental erosion of user trust and a degraded core listening experience, overshadowing the effectiveness of explicit recommendation features.**

### Three Patterns

1.  **Eroding Trust in Content Authenticity and Platform Values**
    Users are increasingly concerned about the proliferation of AI-generated music and Spotify's perceived disregard for fair artist compensation. This skepticism reduces their enthusiasm to explore new content, as they question its origin and the platform's ethical stance, thereby making them less likely to engage with discovery.
    *   *"[appstore | 2026-06-19T02:52:49-07:00 | Sev: 5] "Trust is eroded. ... Not being able to filter out AI generated music..."`
    *   *"[appstore | 2026-06-18T05:57:44-07:00 | Sev: 5] "Soon every real artist will be replace Spotify,Seriously? Its full of ai artist don’t forget that everyone pay your bills are real human being. I am so disappointed"`
    *   *"[appstore | 2026-06-18T08:49:55-07:00 | Sev: 5] "I just wish the musicians received more financial return on each stream."`
    This sentiment, while not explicitly tagged as a major theme, appears strongly in high-severity "other" reviews (part of the 218), indicating a deeper systemic concern that impacts overall platform engagement and willingness to explore.

2.  **Ineffective or Missing Recommendation Feedback Mechanisms**
    Users report that recommended music often doesn't align with their preferences, and critically, they lack clear ways to tell the app what they *dislike*. This absence of explicit negative feedback prevents the recommendation engine from learning and improving, leading to persistent irrelevant suggestions that hinder new music discovery.
    *   *"[appstore | 2026-06-19T03:35:27-07:00 | Sev: 3] "Recommended songs The recommends songs are not based off my wants."`
    *   *"[playstore | 2026-06-19T18:55:22 | Sev: 3] "...there's no way to tell the app "I really don't like this band, stop playing their music""`
    This pattern is directly captured by the "recommendation_quality" theme (9 mentions) and implicitly by "playlist_issues" (14 mentions) where unwanted songs are forced into queues or playlists, making users disengage.

3.  **Core Listening Experience Degraded by Ads and Paywalls**
    Overwhelming ad frequency, aggressive premium paywalls, and restrictions on basic functionalities (like selecting specific songs or looping) create significant user frustration. This degraded experience disincentivizes users from spending time exploring new music, as they are constantly interrupted or blocked from even basic listening, let alone deeper discovery features.
    *   *"[appstore | 2026-06-18T23:45:43-07:00 | Sev: 5] "Meh The music is great, the transitions between songs is okay— but the constant ads are the problem."`
    *   *"[appstore | 2026-06-18T22:51:34-07:00 | Sev: 5] "Pay wall The amount of paywalls this app has is sickening"`
    *   *"[appstore | 2026-06-18T17:07:22-07:00 | Sev: 5] "How come we cant loop a song without premium?? And we cant pick the songs in the playlist without premium,and you also cant play them in order?!?!"`
    This is the most widespread and severe issue, reflected in "ads" (48 mentions) and "pricing" (36 mentions), dominating the high-severity feedback (52 reviews at severity 5, 4 at severity 4).

### One Concrete Implication

Prioritize investment in improving the foundational user experience and rebuilding trust, rather than solely focusing on enhancing existing recommendation algorithms. This means addressing ad frequency/intensity, refining free-tier limitations to be less intrusive, and clearly communicating Spotify's stance and actions regarding AI-generated music and artist compensation. A user less frustrated by the basic experience is more likely to engage with and benefit from discovery features.

---
## 2. What are the most common frustrations with recommendations?

**Frustrations with Spotify's Music Recommendations**

**While overshadowed by more prevalent user complaints regarding ads and pricing, the direct frustrations with Spotify's music recommendations primarily center on the perceived inaccuracy and lack of user control over algorithmic music suggestions.**

### Three Patterns:

1.  **Irrelevant or Mismatched Recommendations**
    Users express frustration when Spotify's algorithmic suggestions fail to align with their personal taste or current listening intent. This includes instances where the system injects "stupid songs" into personal playlists or consistently recommends music that doesn't match their stated "wants."
    *   *“The recommends songs are not based off my wants.”* (appstore | 2026-06-19 | Sev: 3)
    *   *“every time i make a playlist i can’t even listen to it because it adds all of its stupid songs.”* (appstore | 2026-06-18 | Sev: 5)
    This is the most direct frustration with recommendation quality, explicitly identified in 9 reviews tagged under `recommendation_quality`, and echoed in some of the 14 `playlist_issues` where Spotify’s auto-addition of tracks is unwelcome.

2.  **Lack of User Control and Feedback Mechanisms**
    Users feel powerless to influence or filter out specific content from their recommendations or playback queues. This includes a clear desire for features to actively "dislike" artists or bands, or to filter out specific content types like AI-generated music, to prevent unwanted tracks from being repeatedly suggested.
    *   *“there's no way to tell the app "I really don't like this band, stop playing their music"”* (playstore | 2026-06-19 | Sev: 3)
    *   *“Not being able to filter out AI generated music…”* (appstore | 2026-06-19 | Sev: 5)
    This frustration is a key contributor to perceived `recommendation_quality` issues (9 reviews), as poor recommendations are compounded by the inability to correct or prevent their recurrence.

3.  **Algorithmic Stagnation Hindering Genuine Discovery**
    Instead of facilitating new music discovery, the recommendation system is sometimes perceived as repetitive or stagnant. Users report that the algorithm may play overly familiar songs, including the exact track they just searched for, rather than actively introducing new, diverse, and relevant music to expand their listening horizons. For free users, algorithmic mixes that cannot be undone also limit their ability to simply listen to their own music.
    *   *“do not play the same song which is searching”* (playstore | 2026-06-19 | Sev: 3)
    *   *“It’s on mix and I can’t undo it and I don’t wanna pay premium just to listen my music in latest added 😡”* (appstore | 2026-06-19 | Sev: 5)
    This theme is explicitly noted by 1 review under `repeat_play_loop` and implied by issues related to algorithmic "mixes" within `playlist_issues` (14 reviews), indicating a missed opportunity for true discovery.

### One Concrete Implication:

Given that users struggle with both the accuracy of recommendations and their inability to control them, the product team should explore enhancing user feedback mechanisms directly within the playback experience. This could include more prominent "dislike" options for songs/artists, and advanced filtering capabilities for specific content types (e.g., AI-generated music), empowering users to shape their discovery journey more effectively.

---
## 3. What listening behaviors are users trying to achieve?

**Users are striving for an uninterrupted, personalized, and value-driven listening experience, with current pain points severely impeding their ability to effectively discover music.**

Here are three key patterns of desired listening behaviors:

1.  **Uninterrupted Immersion**
    Users seek a seamless listening flow, desiring to engage with music and podcasts without disruptive external factors. They want to get lost in their audio content, whether familiar or new, free from constant commercial breaks or technical impediments.
    *   *"The amount of commercials is insane and inconsistent."* [appstore | 2026-06-19T00:09:09-07:00 | Sev: 5]
    *   *"The music is great... but the constant ads are the problem. Like, I’d be listening to a row of two songs in my queue, and then I’m struck blind by a ROW of FIV..."* [appstore | 2026-06-18T23:45:43-07:00 | Sev: 5]
    *   *"App crashes throughout the day without warning, is extremely slow to l..."* [appstore | 2026-06-18T21:45:36-07:00 | Sev: 5]
    This desire is highly widespread, surfacing in 48 reviews directly related to "ads" and a significant portion of the 218 "other" reviews that detail app performance issues, with many at severity 5.

2.  **Personalized & Controlled Playback**
    Users want precise control over their listening choices and playback experience. This includes playing specific songs, arranging content in a desired order, looping tracks, and actively filtering out unwanted content such as AI-generated music or disliked artists. This level of control is fundamental for intentional music discovery and curation.
    *   *"it’s on mix and I can’t undo it and I don’t wanna pay premium just to listen my music in latest added 😡"* [appstore | 2026-06-19T00:23:52-07:00 | Sev: 5]
    *   *"How come we cant loop a song without premium?? And we cant pick the songs in the playlist without premium,and you also cant play them in order?!?!"* [appstore | 2026-06-18T17:07:22-07:00 | Sev: 5]
    *   *"Not being able to filter out AI generated music..."* [appstore | 2026-06-19T02:52:49-07:00 | Sev: 5]
    This pattern is evident in 14 "playlist_issues" reviews, 9 "recommendation_quality" reviews (often concerning filtering), and many complaints within the "pricing" and "other" categories that highlight paywalls restricting basic playback functionality.

3.  **Value-Driven Access to Content**
    Users expect that their investment (time as a free user, or money as a premium subscriber) should grant them access to a rich content library and robust features without excessive paywalls or a perceived degradation of service. They seek a clear value proposition where increased cost corresponds to improved or retained benefits, which directly impacts their opportunity for discovery.
    *   *"Money hungry app, that constantly increases our Price but doesn’t give us more listening hours on Audiobooks or Ad free Podcasts."* [appstore | 2026-06-18T21:03:47-07:00 | Sev: 5]
    *   *"The amount of paywalls this app has is sickening"* [appstore | 2026-06-18T22:51:34-07:00 | Sev: 5]
    *   *"greedy company. removed my dj x feature on my student plan nou i need to pay 5 times the price just to get it back"* [playstore | 2026-06-19T19:01:36 | Sev: 4]
    This behavior is strongly indicated by 36 "pricing" reviews and frequently intertwined with complaints about "ads" (48 reviews) and a large segment of "other" reviews, signifying widespread frustration over perceived diminishing value, particularly among high-severity reviews.

**Implication for Product Decisions:**
To improve music discovery, the product team must first address the foundational frustrations hindering core listening behaviors. Prioritizing initiatives that ensure an uninterrupted, stable playback experience, grant users greater control over their audio content, and enhance the perceived value of both free and premium tiers will create a more positive environment conducive to users willingly exploring new music on Spotify.

---
## 4. What causes users to repeatedly listen to the same content?

**Users repeatedly listen to the same content not out of preference, but largely due to a degraded free user experience and frustrating premium paywalls that prevent diverse listening, coupled with critical app functionality issues.**

### Patterns

1.  **Aggressive paywalling restricts playback control and choice**
    Free users are severely limited in selecting, skipping, or looping specific tracks, often forced into predetermined mixes or a cycle of listening to a narrow selection. Even for premium users, some features become inaccessible or are removed, causing frustration and hindering personal playlist control. This directly pushes users towards repetitive listening or simply abandoning attempts at new discovery due to lack of agency.

    *   *"[appstore | 2026-06-19T00:23:52-07:00 | Sev: 5] it’s stuck It’s on mix and I can’t undo it and I don’t wanna pay premium just to listen my music in latest added 😡"*
    *   *"[appstore | 2026-06-18T17:07:22-07:00 | Sev: 5] How come we cant loop a song without premium?? And we cant pick the songs in the playlist without premium,and you also cant play them in order?!?!"*
    *   *"[appstore | 2026-06-18T14:17:42-07:00 | Sev: 5] every time i make a playlist i can’t even listen to it because it adds all of its stupid songs."*

    This pattern is widespread, with "pricing" accounting for 36 reviews and many of the 218 "other" reviews, especially high-severity ones, directly mentioning paywalls, inability to control playback, and interference with user-created playlists (part of "playlist_issues" with 14 mentions).

2.  **Excessive and intrusive ads degrade the listening experience**
    Users, both free and (surprisingly) some premium, are subjected to a high volume of advertisements that are long, inconsistently timed, and frequently interrupt the listening experience. This creates significant frustration, making new content exploration unbearable and driving users to stick with familiar content they can tolerate ad interruptions for, or to seek alternative platforms.

    *   *"[appstore | 2026-06-19T00:09:09-07:00 | Sev: 5] Ugh The amount of commercials is insane and inconsistent. To the point I prefer to use YouTube which also has commercials but at least they’re more tolerable and understand how to properly shuffle thr..."*
    *   *"[appstore | 2026-06-18T23:45:43-07:00 | Sev: 5] Meh The music is great, the transitions between songs is okay— but the constant ads are the problem. Like, I’d be listening to a row of two songs in my queue, and then I’m struck blind by a ROW of FIV..."*
    *   *"[appstore | 2026-06-18T04:08:55-07:00 | Sev: 5] Always ads! Have premium and I still get pop ups every time I open the app that I have to dismiss! I’m over it and wonder why I’m paying so much!"*

    "Ads" is the second most frequent explicit theme with 48 mentions, often appearing in the highest-severity feedback. This suggests a significant barrier to enjoyable and diverse listening.

3.  **Poor app stability and recommendation quality hinder discovery**
    Users encounter fundamental app issues such as frequent crashes, slow loading times, and unresponsive playback controls, making the application unreliable for any active listening. Furthermore, a perceived lack of relevant music recommendations makes it difficult for users to naturally discover new content, leading them to stay within their comfort zone of known songs or give up on exploring altogether.

    *   *"[appstore | 2026-06-18T21:45:36-07:00 | Sev: 5] Has been getting worse and worse Since a few updates ago the app is nearly unusable. I’m on a fairly new iPhone 13 (all updated). App crashes throughout the day without warning, is extremely slow to l..."*
    *   *"[appstore | 2026-06-19T03:35:27-07:00 | Sev: 3] Recommended songs The recommends songs are not based off my wants."*
    *   *"[appstore | 2026-06-18T07:56:43-07:00 | Sev: 5] I’ve never had this issue before, but for some reason I can’t replay songs because the song bar won’t move how much I tap on it, and the rewind button is greye..."*

    While "recommendation_quality" directly accounts for 9 reviews, numerous high-severity reviews in the "other" category (218 reviews total) describe critical app stability issues that make engaging with any content, let alone new content, frustrating and unreliable.

### Concrete Implication

Product decisions should prioritize improving the baseline user experience, particularly for free users, by re-evaluating aggressive paywalling and ad frequency to foster an environment conducive to organic discovery rather than frustrating it. Simultaneously, core app stability and reliable playback controls must be a top development priority to ensure a functional and enjoyable platform for all users.

---
## 5. What unmet needs emerge consistently across reviews?

**The fundamental unmet need consistently emerging across reviews is a pervasive dissatisfaction with Spotify's core listening experience due to excessive monetization, leading to a perceived degradation of value and user control.**

### Three Patterns

1.  **Diminished Core Listening Experience (Free & Premium)**
    *   **What it means in user terms:** Users, both free and paying, express deep frustration with an intrusive ad experience and critical playback features being arbitrarily paywalled. They feel they cannot simply listen to music how they want without constant interruption or being forced to upgrade for basic functionalities like picking songs or looping.
    *   **Evidence:**
        *   *"[AppStore | 2026-06-19T00:24:31-07:00 | Sev: 5] Why am I seeing three ads before a podcast, which has three more ads when paying for Spotify?????"*
        *   *"[AppStore | 2026-06-18T23:45:43-07:00 | Sev: 5] the constant ads are the problem. Like, I’d be listening to a row of two songs in my queue, and then I’m struck blind by a ROW of FIV..."*
        *   *"[AppStore | 2026-06-18T17:07:22-07:00 | Sev: 5] How come we cant loop a song without premium?? And we cant pick the songs in the playlist without premium,and you also cant play them in order?!?!"*
        *   *"[AppStore | 2026-06-18T14:17:42-07:00 | Sev: 5] every time i make a playlist i can’t even listen to it because it adds all of its stupid songs."*
    *   **How widespread it is based on the data:** Extremely widespread. "Ads" accounts for 48 reviews, "pricing" (often tied to paywalls) for 36, and a significant portion of the 218 "other" reviews, along with many high-severity verbatims, highlight this core friction.

2.  **Eroding Trust in Content Quality and Personalization Control**
    *   **What it means in user terms:** Users are losing trust in the quality and relevance of the content offered, fearing an influx of unwanted or AI-generated music, and feel a lack of control over what they are recommended or forced to hear. This directly impacts their ability to discover *desirable* music.
    *   **Evidence:**
        *   *"[AppStore | 2026-06-19T02:52:49-07:00 | Sev: 5] Not being able to filter out AI generated music..."*
        *   *"[AppStore | 2026-06-18T05:57:44-07:00 | Sev: 5] Its full of ai artist don’t forget that everyone pay your bills are real human being."*
        *   *"[AppStore | 2026-06-18T14:17:42-07:00 | Sev: 5] every time i make a playlist i can’t even listen to it because it adds all of its stupid songs."*
        *   *"[AppStore | 2026-06-19T03:35:27-07:00 | Sev: 3] The recommends songs are not based off my wants."*
        *   *"[PlayStore | 2026-06-19T18:55:22 | Sev: 3] also, there's no way to tell the app "I really don't like this band, stop playing their music""*
    *   **How widespread it is based on the data:** While "recommendation_quality" (9 reviews) and "playlist_issues" (14 reviews) are lower numerically, the sentiment regarding AI content (falling under "other") and unwanted additions to playlists signifies a critical, high-severity concern about content authenticity and user agency in curation, which fundamentally underpins successful discovery.

3.  **App Performance and Usability Degradation**
    *   **What it means in user terms:** Beyond content, users are experiencing basic functional failures: the app is slow, crashes, or specific content types (like podcasts or audiobooks) are buggy, making the overall experience frustrating and unreliable.
    *   **Evidence:**
        *   *"[AppStore | 2026-06-18T21:45:36-07:00 | Sev: 5] App crashes throughout the day without warning, is extremely slow to l..."*
        *   *"[AppStore | 2026-06-18T21:02:54-07:00 | Sev: 5] When you click on a podcast page, it doesn’t load the sh..."*
        *   *"[AppStore | 2026-06-18T15:44:50-07:00 | Sev: 5] My audiobooks keeps repeating chapters."*
        *   *"[AppStore | 2026-06-18T08:08:48-07:00 | Sev: 5] It is severely laggy at startup."*
    *   **How widespread it is based on the data:** Several high-severity reviews highlight these functional issues, which are likely categorized within the large "other" theme (218 reviews), indicating a significant unaddressed technical debt and usability friction.

### Concrete Implication

The Growth PM should prioritize addressing the foundational issues of ad intrusiveness, perceived value for money, and user control over the core listening experience. Users struggling with excessive ads, paywalls for basic functionality, and unreliable app performance are unlikely to engage positively with new music discovery features. Specifically for discovery, empower users with more explicit tools to filter out unwanted content (e.g., AI music, specific artists) and provide clearer feedback mechanisms for recommendations, fostering trust and a sense of agency that is critical for meaningful music exploration.
