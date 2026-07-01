# Spotify Discovery Insights Report
*Generated on 2026-06-23*

## Concluding Section: Accelerating Music Discovery on Spotify

### 1. Executive Summary

Spotify users are consistently frustrated with their music discovery experience, primarily because the platform often delivers irrelevant or unwanted recommendations while simultaneously restricting fundamental listening controls. This pervasive issue erodes user trust and enjoyment, leading to a stagnant, repetitive listening cycle rather than active exploration. Both free and premium users feel a diminished sense of control over their personalized content, are frequently interrupted by ads or technical glitches, and perceive a declining value proposition. Addressing these foundational user experience barriers is critical to fostering a more engaging and effective discovery environment.

### 2. Top 3 Unmet Needs

1.  **Empowered Content Curation and Control:** Users deeply desire granular control over what music they encounter. They need robust tools to explicitly filter out undesired content (such as AI-generated music or specific artists/genres) and more effective mechanisms to steer recommendations away from irrelevant or repetitive suggestions, ultimately trusting that Spotify understands and respects their unique tastes.
2.  **Unrestricted Exploration and Playback Agency:** Users crave an uninterrupted listening experience and basic control over their music. For free users, the inability to select specific songs, manage playback order, or loop tracks creates a passive, frustrating environment that actively deters exploration. Even premium users feel their experience is undermined by unexpected ads or a perceived lack of value for their subscription.
3.  **Reliable and Trustworthy Platform Experience:** Beyond content and control, users expect a stable, high-performing application that consistently delivers on its promise. Frequent app crashes, slow loading times, and broken playback features diminish overall satisfaction and willingness to engage. This also extends to a need for greater transparency and trust regarding content quality and the value provided for their investment.

### 3. Recommended Next Steps

To address these critical unmet needs and revitalize music discovery, we recommend the following product and growth experiments:

1.  **Granular Content Filtering & Dislike Mechanism:**
    *   **Experiment Idea:** Introduce an "Exclude Artist/Genre" feature (similar to 'Don't play this song/artist') and a "Filter Content Type" option (e.g., "Hide AI-generated music") accessible directly from playback and discovery surfaces for all users.
    *   **Measurement:** Track usage of these new controls, measure subsequent user satisfaction with recommendations, and monitor changes in discovery playlist engagement (e.g., "Discover Weekly," "Release Radar") for users who utilize these filters.
    *   **Goal:** Empower users to actively shape their discovery feed, increasing relevance and trust.

2.  **Strategic Free Tier Playback Flexibility:**
    *   **Experiment Idea:** A/B test unlocking a limited number of "on-demand" plays per day (e.g., 5-10 songs) specifically for user-created playlists on the free tier, or introduce a basic "mini-queue" feature for up to 3-5 songs.
    *   **Measurement:** Analyze the impact on free user engagement, retention rates, and, critically, premium conversion rates. Monitor if this limited flexibility encourages more active exploration within their own curated content.
    *   **Goal:** Reduce friction for free users to actively explore and enjoy their music, potentially driving a clearer path to premium value.

3.  **Premium Experience Enhancement & Ad Re-evaluation:**
    *   **Experiment Idea:** Implement an A/B test to completely eliminate all internal "house" ads (e.g., podcast ads, pop-ups promoting Spotify features) for Premium subscribers. Simultaneously, conduct a separate test to slightly reduce the ad frequency for free users while maintaining or slightly increasing the ad break length.
    *   **Measurement:** For Premium users, track retention rates, customer sentiment, and overall satisfaction. For free users, monitor engagement metrics, ad revenue per user, and feedback related to ad experience.
    *   **Goal:** Restore the perceived value and premium feel for paying subscribers, while finding a more balanced and less intrusive ad experience for free users to encourage sustained engagement.

---

## 1. Why do users struggle to discover new music?

Here's an analysis of user struggles with new music discovery on Spotify:

**Users struggle to discover new music primarily because the platform dilutes genuine recommendations with unwanted content, provides insufficient personalization controls, and locks essential exploration features behind paywalls.**

### Three Patterns of Struggle

1.  **Unwanted Content and Dilution of Discovery**
    Users are frustrated by the presence of content they actively dislike or perceive as inauthentic (e.g., AI-generated music), or find their curated playlists overridden with "stupid songs." This makes it frustrating to sift through and discover desirable new artists or tracks, eroding trust in the platform's curation.
    *   _"[appstore | 2026-06-19T02:52:49-07:00 | Sev: 5] Trust is eroded. ...Not being able to filter out AI generated music..."_
    *   _"[appstore | 2026-06-18T05:57:44-07:00 | Sev: 5] Soon every real artist will be replace Spotify,Seriously? Its full of ai artist..."_
    *   _"[appstore | 2026-06-18T14:17:42-07:00 | Sev: 5] greedy, greedy people every time i make a playlist i can’t even listen to it because it adds all of its stupid songs."_
    *   **Widespread:** While not a distinct theme category, these specific complaints appear in high-severity reviews, including 2 explicit mentions of AI music and 1 explicit mention of unwanted songs being added to user playlists. These issues likely contribute to the large "other" theme (218 reviews).

2.  **Ineffective and Uncontrollable Recommendations**
    Users feel that Spotify's algorithmic recommendations are often irrelevant to their actual tastes. Crucially, they lack clear mechanisms to provide effective negative feedback or refine what they *don't* want to hear, leading to a stagnant and frustrating discovery experience where new music isn't aligned with their preferences.
    *   _"[appstore | 2026-06-19T03:35:27-07:00 | Sev: 3] Recommended songs The recommends songs are not based off my wants."_
    *   _"[playstore | 2026-06-19T18:55:22 | Sev: 3] ...there's no way to tell the app "I really don't like this band, stop playing their music""_
    *   **Widespread:** This is directly reflected in the `recommendation_quality` (9 reviews) and `mood_matching` (2 reviews) themes, accounting for 11 reviews that specifically call out the lack of quality or control in recommendations.

3.  **Paywalls Restricting Free-Tier Exploration**
    Basic playback control features, such as selecting specific songs from a playlist, playing them in order, or moving out of a mixed shuffle, are gated behind a premium subscription. This prevents free users from actively exploring new artists or albums in a structured way, effectively trapping them in a passive listening loop where active discovery is severely hampered.
    *   _"[appstore | 2026-06-18T17:07:22-07:00 | Sev: 5] ...we cant pick the songs in the playlist without premium,and you also cant play them in order?!?!"_
    *   _"[appstore | 2026-06-19T00:23:52-07:00 | Sev: 5] it’s stuck It’s on mix and I can’t undo it and I don’t wanna pay premium just to listen my music in latest added 😡"_
    *   _"[playstore | 2026-06-19T18:43:04 | Sev: 4] ...I'm in a mobile and i can't loop songs unless i have premium..."_
    *   **Widespread:** This issue is central to many complaints related to `pricing` (36 reviews) and `playlist_issues` (14 reviews), as well as general "paywall" frustrations under "other." Several high-severity reviews explicitly mention these playback limitations, indicating a significant blocker for free user discovery.

### Concrete Implication for Product Decisions

To significantly improve music discovery, Spotify should prioritize enhancing content quality control by implementing clear labeling or filtering options for AI-generated music and eliminating unwanted playlist injections. Simultaneously, empowering users with more granular control over recommendations, such as explicit "dislike" functionality across all tiers, is critical. For the free tier, consider strategically unlocking limited on-demand playback or queue management features to enable more active, user-driven exploration of new music without a full premium commitment.

---
## 2. What are the most common frustrations with recommendations?

Here's an analysis of user frustrations with music recommendations based on the provided data:

**While not the most frequent complaint overall, the primary frustrations with Spotify's music recommendations revolve around their perceived irrelevance, interference with user-curated content, and lack of user control over content filters.**

### Three Patterns

1.  **Irrelevant or Unmatched Recommendations**
    *   **What it means in user terms:** Users feel that the recommended songs or mixes do not align with their personal preferences or current listening needs. They also express a desire for more direct ways to signal their dislike for specific artists or tracks to improve future recommendations.
    *   **Evidence:**
        *   *“Recommended songs are not based off my wants. Too many ads and the price is too high…”* (appstore | 2026-06-19T03:35:27-07:00 | Sev: 3)
        *   *“also, there's no way to tell the app "I really don't like this band, stop playing their music"* (playstore | 2026-06-19T18:55:22 | Sev: 3)
    *   **How widespread it is based on the data:** This concern is explicitly captured by the "recommendation_quality" (9 reviews) and "mood_matching" (2 reviews) themes, totaling 11 out of 344 reviews. This indicates a quality gap for a small but vocal segment of users.

2.  **Recommendations Interfering with User-Curated Playlists**
    *   **What it means in user terms:** Users are frustrated when Spotify's algorithmic suggestions or "mix" features automatically add unwanted songs to their personal playlists, diminishing their control and enjoyment of their own carefully selected music. This can be exacerbated by paywalls preventing easy removal or reordering.
    *   **Evidence:**
        *   *“greedy, greedy people every time i make a playlist i can’t even listen to it because it adds all of its stupid songs. they should make the free one better smh. do not recommend. why are they so greedy…”* (appstore | 2026-06-18T14:17:42-07:00 | Sev: 5)
        *   *“it’s stuck It’s on mix and I can’t undo it and I don’t wanna pay premium just to listen my music in latest added 😡”* (appstore | 2026-06-19T00:23:52-07:00 | Sev: 5)
    *   **How widespread it is based on the data:** This issue falls under "playlist_issues" (14 reviews), with at least two high-severity verbatims directly linking algorithmic interference to user-created content.

3.  **Lack of Control Over Content Quality (e.g., AI-Generated Music)**
    *   **What it means in user terms:** Users express a loss of trust and dissatisfaction when they cannot filter out specific types of content, such as AI-generated music, from their listening experience. This implies a desire for greater transparency and control over the origin and quality of music being surfaced or recommended.
    *   **Evidence:**
        *   *“Trust is eroded. After years I unsubscribed to Spotify premium. Not being able to filter out AI generated music, learning about the abhorrent and blatant bottom line mission this company is on - just ...”* (appstore | 2026-06-19T02:52:49-07:00 | Sev: 5)
        *   *“Soon every real artist will be replace Spotify,Seriously? Its full of ai artist don’t forget that everyone pay your bills are real human being. I am so disappointed”* (appstore | 2026-06-18T05:57:44-07:00 | Sev: 5)
    *   **How widespread it is based on the data:** While categorized under "other" (218 reviews), the concern about filtering AI-generated music is mentioned by at least two high-severity users, highlighting a qualitative concern about content presented within the discovery experience.

### One Concrete Implication

To improve user satisfaction with music discovery, the product team should invest in features that empower users with more granular control over their listening experience. This includes developing explicit "dislike" or "do not play artist/genre" functionalities, providing clear options to prevent algorithmic additions to personal playlists, and exploring tools to filter or label content based on its origin, such as AI-generated music. Enhancing these control mechanisms can boost perceived recommendation quality and user trust.

---
## 3. What listening behaviors are users trying to achieve?

**Users primarily seek an uninterrupted, personalized, and stable listening experience, demanding full control over their content and playback without excessive paywalls or technical disruptions.**

### Three Patterns of Desired Listening Behaviors:

1.  **Uninterrupted and Ad-Free Immersion**
    Users are trying to achieve a listening flow where their experience is not broken by frequent or lengthy advertisements, especially when consuming podcasts or paying for a premium service. They express frustration when pop-ups or ads appear even with a subscription, or when ad frequency on the free tier becomes intolerable, making them prefer alternative services.

    *   *“Why am I seeing three ads before a podcast, which has three more ads when paying for Spotify??????”* [appstore | 2026-06-19T00:24:31-07:00 | Sev: 5]
    *   *“The amount of commercials is insane and inconsistent.”* [appstore | 2026-06-19T00:09:09-07:00 | Sev: 5]
    *   *“Always ads! Have premium and I still get pop ups every time I open the app that I have to dismiss!”* [appstore | 2026-06-18T04:08:55-07:00 | Sev: 5]
    *   **Widespread Impact:** This is a highly prevalent issue, explicitly mentioned in 48 reviews related to "ads," and implicitly in many "pricing" complaints where users expect an ad-free experience for their subscription.

2.  **Personalized and Controlled Content Curation**
    Users desire complete agency over what they listen to, including the ability to play specific songs from their own playlists, determine playback order, loop tracks, and actively filter out unwanted content like AI-generated music. They feel undermined when the app automatically adds "stupid songs" to their playlists or restricts basic playback controls like looping and explicit song selection behind a paywall.

    *   *“How come we cant loop a song without premium?? And we cant pick the songs in the playlist without premium,and you also cant play them in order?!?!”* [appstore | 2026-06-18T17:07:22-07:00 | Sev: 5]
    *   *“every time i make a playlist i can’t even listen to it because it adds all of its stupid songs.”* [appstore | 2026-06-18T14:17:42-07:00 | Sev: 5]
    *   *“Not being able to filter out AI generated music, learning about the abhorrent and blatant bottom line mission this company is on - just ...”* [appstore | 2026-06-19T02:52:49-07:00 | Sev: 5]
    *   **Widespread Impact:** This behavior is highly desired, evidenced by 14 mentions of "playlist_issues" and explicit demands for basic playback control (looping, specific song selection) being restricted. Many "other" and "pricing" complaints also stem from the inability to control the listening experience.

3.  **Reliable and Seamless App Performance**
    Users expect a foundational level of application stability and responsiveness. They want the app to load quickly, function without crashing, and execute features reliably across all their devices. Technical glitches, slow startups, or broken functionalities directly hinder their ability to engage in any desired listening behavior.

    *   *“App crashes throughout the day without warning, is extremely slow to l...”* [appstore | 2026-06-18T21:45:36-07:00 | Sev: 5]
    *   *“My audiobooks keeps repeating chapters. Has been happening for about a month. Can’t seem to be able to fix it. Glitch in the app!”* [appstore | 2026-06-18T15:44:50-07:00 | Sev: 5]
    *   *“Laggy Startup It is severely laggy at startup. It takes several minutes to load up after opening and is super slow.”* [appstore | 2026-06-18T08:08:48-07:00 | Sev: 5]
    *   **Widespread Impact:** While not a dedicated theme, these critical performance issues frequently appear in high-severity reviews categorized under "other" (218 reviews), indicating that basic app functionality is a significant and widespread concern that impacts the user's ability to listen at all.

### One Concrete Implication:

To address core user dissatisfaction and foster growth, Spotify must prioritize restoring fundamental listening controls and reducing friction in the user experience across all tiers. This means re-evaluating the free tier's limitations on basic playback (e.g., looping, specific song selection), significantly reducing ad load and frequency for both free and premium users, and investing heavily in core app stability and performance to ensure a reliable and seamless listening environment.

---
## 4. What causes users to repeatedly listen to the same content?

**Users repeatedly listen to the same content primarily due to a frustrating and restrictive user experience, driven by aggressive paywalls, excessive ads, and core app malfunctions that actively deter exploration and new music discovery.**

Here are three patterns that explain why users fall into repetitive listening habits:

### 1. Restrictive Paywalls for Basic Playback Controls

**What it means in user terms:** Free users, and some premium users, feel actively prevented from exercising fundamental control over their listening experience. They cannot select specific songs, play them in a chosen order, or even loop tracks. This pushes them towards default mixes or replaying known content where they might have some semblance of control or familiarity, as venturing into new, uncontrolled mixes is too frustrating.

**Evidence:**
*   _"[appstore | 2026-06-19T00:23:52-07:00 | Sev: 5] it’s stuck It’s on mix and I can’t undo it and I don’t wanna pay premium just to listen my music in latest added 😡"_
*   _"[appstore | 2026-06-18T17:07:22-07:00 | Sev: 5] So money hungry How come we cant loop a song without premium?? And we cant pick the songs in the playlist without premium,and you also cant play them in order?!?!"_
*   _"[appstore | 2026-06-18T14:17:42-07:00 | Sev: 5] greedy, greedy people every time i make a playlist i can’t even listen to it because it adds all of its stupid songs."_

**How widespread it is:** Explicit mentions of "pricing" total 36, and many high-severity "other" complaints (218 total) are clearly related to paywalls and feature limitations. This severely impacts a core listening experience for a significant user segment.

### 2. Overbearing Advertising and Performance Instability

**What it means in user terms:** Users, including some who pay for Premium, are constantly interrupted by frequent and lengthy ads, or they struggle with a slow, buggy application. This degraded experience makes the process of experimenting with new music or simply browsing for discovery feel too burdensome, leading users to stick with familiar, reliable tracks to minimize frustrating interruptions.

**Evidence:**
*   _"[appstore | 2026-06-19T00:09:09-07:00 | Sev: 5] Ugh The amount of commercials is insane and inconsistent."_
*   _"[appstore | 2026-06-18T21:45:36-07:00 | Sev: 5] App crashes throughout the day without warning, is extremely slow to l..."_
*   _"[appstore | 2026-06-18T04:08:55-07:00 | Sev: 5] Always ads! Have premium and I still get pop ups every time I open the app that I have to dismiss!"_

**How widespread it is:** "Ads" is a prominent theme with 48 explicit mentions. General app performance issues are also prevalent within the large "other" category (218 mentions), supported by numerous 'Sev: 5' complaints. This friction impacts a broad user base, regardless of subscription status.

### 3. Inaccurate or Malfunctioning Discovery and Playback Features

**What it means in user terms:** When algorithmic recommendations fail to align with user preferences, or when fundamental playback controls like looping or shuffling behave erratically, users lose trust in Spotify's ability to provide a satisfying, novel listening experience. This directly causes them to revert to manually replaying known songs or playlists, as venturing into new, uncurated content becomes an unreliable gamble.

**Evidence:**
*   _"[appstore | 2026-06-19T03:35:27-07:00 | Sev: 3] Recommended songs The recommends songs are not based off my wants."_
*   _"[playstore | 2026-06-19T18:54:28 | Sev: 3] do not play the same song which is searching"_
*   _"[appstore | 2026-06-18T15:44:50-07:00 | Sev: 5] Audiobooks faulty My audiobooks keeps repeating chapters."_

**How widespread it is:** While less frequently cited compared to ads or pricing, "recommendation_quality" (9 mentions), "playlist_issues" (14 mentions), and "repeat_play_loop" (1 mention) directly address the core mechanisms of discovery and controlled playback. The high-severity audiobook example highlights that even fundamental repetition control can be broken, influencing user behavior.

### One Concrete Implication

To effectively encourage music discovery and reduce unwanted content repetition, the product team must prioritize improving the foundational user experience. This includes a strategic re-evaluation of the current paywall model for basic playback controls (like song selection and looping), a significant reduction in ad frequency and intrusiveness across all tiers, and robust efforts to enhance overall app stability and performance. Lowering these points of friction will make users more willing and able to explore new content beyond their current rotation.

---
## 5. Which user segments experience different discovery challenges?

**Core frustrations with excessive monetization and perceived feature degradation severely impede music discovery for both free and paid users, often overshadowing direct algorithmic issues.**

### Three Patterns

1.  **Restricted Agency for Free Users**
    For users on the free tier, the primary discovery challenge isn't about finding new music, but being unable to meaningfully control their basic listening experience. Constant ads, lack of specific song selection, and forced shuffled playback create a frustrating environment where basic enjoyment is elusive, leaving no room for deliberate exploration.
    *   *"[appstore | 2026-06-19T00:23:52-07:00 | Sev: 5] it’s stuck It’s on mix and I can’t undo it and I don’t wanna pay premium just to listen my music in latest added 😡"*
    *   *"[appstore | 2026-06-18T17:07:22-07:00 | Sev: 5] How come we cant loop a song without premium?? And we cant pick the songs in the playlist without premium,and you also cant play them in order?!?!"*
    *   *"[appstore | 2026-06-18T14:17:42-07:00 | Sev: 5] every time i make a playlist i can’t even listen to it because it adds all of its stupid songs."*
    This pattern is highly widespread, reflected in 48 reviews mentioning "ads" and 36 for "pricing," alongside numerous high-severity verbatim complaints about paywalls and feature limitations.

2.  **Erosion of Trust and Value for Premium Users**
    Paid subscribers face discovery challenges stemming from a feeling of eroded trust and diminishing value. They report experiencing ads despite paying, unjustified price increases, and a proliferation of content they deem low-quality or inauthentic (e.g., AI-generated music). This leads to a cynical view of the platform, reducing their willingness to engage with any content, including new discoveries.
    *   *"[appstore | 2026-06-19T02:52:49-07:00 | Sev: 5] Trust is eroded. After years I unsubscribed to Spotify premium. Not being able to filter out AI generated music..."*
    *   *"[appstore | 2026-06-19T00:24:31-07:00 | Sev: 5] Paid subscription Why am I seeing three ads before a podcast, which has three more ads when paying for Spotify?????"*
    *   *"[appstore | 2026-06-18T17:49:42-07:00 | Sev: 5] Same service new price Nothing has changed nothing has been improved and they just keep upping the subscription price."*
    This sentiment is prominent in many of the 52 high-severity (Sev 5) reviews, particularly those from Premium users frustrated by ads and pricing, and explicit mentions of AI content.

3.  **Algorithmic Frustration and Lack of Steering Control**
    Users across both tiers express direct dissatisfaction with the recommendation system, finding it ineffective or unresponsive to their preferences. They struggle to guide the algorithm away from disliked content or to prevent repetitive suggestions, leading to a stagnant or irrelevant discovery experience.
    *   *"[playstore | 2026-06-19T18:55:22 | Sev: 3] ...there's no way to tell the app "I really don't like this band, stop playing their music""*
    *   *"[playstore | 2026-06-19T18:54:28 | Sev: 3] do not play the same song which is searching"*
    *   *"[appstore | 2026-06-19T03:35:27-07:00 | Sev: 3] Recommended songs The recommends songs are not based off my wants."*
    While fewer in direct volume (9 for "recommendation_quality," 2 for "mood_matching," 1 for "repeat_play_loop," and some "playlist_issues"), these complaints represent direct challenges to effective music discovery mechanisms within the app.

### One Concrete Implication

Before investing heavily in nuanced discovery algorithm improvements, product efforts should first address the foundational user experience barriers. Resolving core pain points like excessive ads for free users, perceived premium value erosion, and basic playback control will create a more receptive environment where users are willing and able to engage with discovery features effectively.

---
## 6. What unmet needs emerge consistently across reviews?

**Users are consistently frustrated by a lack of control over their music discovery experience, leading to irrelevant content, unwanted interruptions, and a diminished sense of trust in Spotify's curation.**

### Three Patterns of Unmet Discovery Needs:

1.  **Quality Control over Discovered Content**
    Users are seeking assurances about the authenticity and quality of the music they discover, expressing a strong desire to filter out content they deem undesirable, such as AI-generated music. This reflects a concern that the integrity of their discovery feed is being compromised.
    *   _“Not being able to filter out AI generated music, learning about the abhorrent and blatant bottom line mission this company is on - just ...”_ (appstore | 2026-06-19 | Sev: 5)
    *   _“Its full of ai artist don’t forget that everyone pay your bills are real human being. I am so disappointed”_ (appstore | 2026-06-18 | Sev: 5)
    This emerging concern, while specific in these verbatims, represents a high-severity unmet need that likely falls under the broad "other" category (218 reviews) but directly impacts the perceived quality of new music discovery.

2.  **Irrelevant Recommendations and Lack of Feedback Mechanisms**
    Users feel that Spotify’s algorithmic recommendations often fail to align with their actual preferences, and they lack effective tools to explicitly steer or refine these recommendations. This indicates a frustration with passive discovery and an unmet need for more active, granular control over what is suggested.
    *   _“The recommends songs are not based off my wants.”_ (appstore | 2026-06-19 | Sev: 3)
    *   _“...there's no way to tell the app "I really don't like this band, stop playing their music"”_ (playstore | 2026-06-19 | Sev: 3)
    This pattern is directly captured by the "recommendation_quality" theme (9 reviews) and contributes to "playlist_issues" (14 reviews) when unwanted content appears. It represents a consistent moderate-to-severe pain point.

3.  **Forced & Undesirable "Discovery" in the Free Tier**
    Free users express significant frustration when Spotify forces unwanted or "stupid" songs into their listening experience, particularly within their own self-curated playlists. This diminishes their agency and transforms discovery from an opportunity into an imposed nuisance, especially given the inability to directly select tracks without a premium subscription.
    *   _“...every time i make a playlist i can’t even listen to it because it adds all of its stupid songs.”_ (appstore | 2026-06-18 | Sev: 5)
    *   _“How come we cant loop a song without premium?? And we cant pick the songs in the playlist without premium,and you also cant play them in order?!?!”_ (appstore | 2026-06-18 | Sev: 5)
    This issue is prevalent, reflected in "pricing" (36 reviews) and "playlist_issues" (14 reviews), with many high-severity (Sev 5) complaints indicating a core unmet need for basic control over one's own listening and discovery in the free experience.

### One Concrete Implication for Product Decisions:

To improve user satisfaction and potentially drive premium conversions, Spotify must empower users with greater control over their discovery experience. This includes providing tools to filter undesired content (like AI-generated music), implementing robust feedback mechanisms to refine recommendations, and offering more agency to free users over the content played within their self-curated playlists.
