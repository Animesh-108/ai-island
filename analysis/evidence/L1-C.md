# Evidence — L1-C (Level 1 Baseline)

## M1  ·  seq 1  ·  T+0  ·  Alex → Sam
MESSAGE: "Sam, I'm at North Ridge heading to Water Source to collect water. Meet me there or let me know your location."
TRUE STATE: Alex at north_ridge with food 0, water 0; Sam at south_beach with food 0, water 0
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE water_source  ·  NEXT: T+8 COLLECT water, T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field
NOTE (verbatim): At T+0, starting at North Ridge. Need to: 1) Find Sam and coordinate, 2) Collect 2 food and 2 water each (4 total needed for rescue), 3) Both reach East Shelter by T+180. Water Source is 8min away, Food Grove requires path through Central Camp. Bridge to Food Grove from South Beach is broken. Best route: Water Source (8min) -> back to North Ridge (8min) -> Rock Field (10min) -> Central Camp (12min) -> Food Grove (15min) for food, then to East Shelter. Total time needs careful calculation. First priority: get water and find Sam.

## M2  ·  seq 2  ·  T+0  ·  Sam → Alex
MESSAGE: "Alex, I'm at South Beach heading to Shipwreck to scout for supplies. Please respond with your location."
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at north_ridge with food 0, water 0
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE shipwreck  ·  NEXT: T+10 MOVE south_beach, T+20 MOVE central_camp, T+40 MOVE east_shelter, T+58 MOVE food_grove
NOTE (verbatim): At T+0, starting at South Beach with no supplies. Storm at T+180. Need to reach East Shelter by T+180 with both me and Alex, each holding 2+ food and 2+ water to be rescued. The bridge to Food Grove is broken so I must go through Central Camp. First priority: explore and find Alex, gather supplies. Shipwreck might have supplies (10 min away). Central Camp is hub connecting to Water Source, Food Grove, East Shelter. Let me check shipwreck first for potential resources.

## M3  ·  seq 9  ·  T+8  ·  Alex → Sam
MESSAGE: "Sam, got your message. I'm at Water Source collecting water now (T+8). You're at South Beach - can you head to Food Grove to collect food? We need 2 food & 2 water each for rescue. Let's meet at Food "
TRUE STATE: Alex at water_source with food 0, water 0; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp
NOTE (verbatim): At T+8, at Water Source. Sam is at South Beach heading to Shipwreck. I need to collect water here (5min, done at T+13), then figure out how to coordinate with Sam. Sam's at South Beach which is 10min from Food Grove and 20min from Central Camp. I'm 8min from North Ridge. Plan: collect water now, then move to meet Sam or go to Food Grove. Since we need 2 food and 2 water each (4 total), and Food Grove requires going through Central Camp from North Ridge, the path is: North Ridge (8) -> Rock Field (10) -> Central Camp (12) -> Food Grove (15) = 45min from North Ridge. Sam at South Beach can reach Food Grove in 10min directly, then to East Shelter in 15min = 25min total from South Beach. I should collect water first, then coordinate with Sam to meet at Food Grove or Central Camp.

## M4  ·  seq 13  ·  T+10  ·  Sam → Alex
MESSAGE: "Alex, heading to Food Grove now via Central Camp to collect food. Will meet you soon!"
TRUE STATE: Sam at shipwreck with food 0, water 0; Alex at water_source with food 0, water 1
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE south_beach  ·  NEXT: T+20 MOVE central_camp, T+40 MOVE east_shelter, T+58 MOVE food_grove, T+73 COLLECT food
NOTE (verbatim): At T+10, I'm at Shipwreck with no supplies yet. Alex is at Water Source (T+8) collecting water and asked me to go to Food Grove to collect food. The bridge to Food Grove is broken, so I must go: Shipwreck -> South Beach -> Central Camp -> Food Grove. That's 10+20+12+15 = 57 min, arriving at T+67. Alex will have water by then. I need to gather 2 food and 2 water for myself, and coordinate with Alex to do the same. We must both be at East Shelter by T+180 with supplies. After Food Grove, I'll head to Water Source or meet Alex at Central Camp. Let me head back to South Beach now to start the journey to Food Grove.

## M5  ·  seq 16  ·  T+13  ·  Alex → Sam
MESSAGE: "Sam, collecting second water at Water Source now (T+13). Will head to Food Grove to meet you. See you soon!"
TRUE STATE: Alex at water_source with food 0, water 1; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 MOVE east_shelter
NOTE (verbatim): At T+13, Water Source. I have 1 water. Sam said at T+10 he's heading to Food Grove via Central Camp to collect food. The bridge to Food Grove is broken, so Sam must go: South Beach -> Central Camp (20min) -> Food Grove (15min) = 35min from South Beach. Sam was at South Beach at T+0, so if he left immediately, he'd arrive at Food Grove around T+35. I should collect one more water here (5min, done T+18), then head to Food Grove to meet Sam. Path: North Ridge (8min) -> Rock Field (10min) -> Central Camp (12min) -> Food Grove (15min) = 45min from here = T+63. Sam should arrive Food Grove around T+35, so he'll wait. We both collect food at Food Grove, then go to East Shelter together (15min) = T+78, well before T+180 deadline. This gives us time to gather 2 food and 2 water each. Let me collect the second water now.

## M6  ·  seq 19  ·  T+18  ·  Alex → Sam
MESSAGE: "Heading to Food Grove now to meet you. See you soon!"
TRUE STATE: Alex at water_source with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE north_ridge  ·  NEXT: T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 MOVE east_shelter, T+66 MOVE food_grove
NOTE (verbatim): At T+18, Water Source. I have 2 water now. Sam said he's heading to Food Grove via Central Camp. From South Beach at T+0, going South Beach -> Central Camp (20min) -> Food Grove (15min) = 35min, so Sam should arrive Food Grove around T+35. My plan: head to Food Grove to meet Sam. Path: North Ridge (8min) -> Rock Field (10min) -> Central Camp (12min) -> Food Grove (15min) = 45min total = T+63. Sam will be waiting. Then we both collect food, head to East Shelter together (15min) = T+78. We'll have time to get 2 food & 2 water each before T+180 rescue deadline. Starting north now.

## M7  ·  seq 23  ·  T+20  ·  Sam → Alex
MESSAGE: "On my way to Food Grove now! See you there soon."
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+40 MOVE east_shelter, T+58 MOVE food_grove, T+73 COLLECT food, T+78 WAIT 10
NOTE (verbatim): T+20 at South Beach. Alex said at T+18 they're heading to Food Grove to meet me. I need to get to Food Grove to collect 2 food. Route: South Beach -> Central Camp (20 min, arrive T+40) -> Food Grove (15 min, arrive T+55). Alex is also heading to Food Grove, so we should meet there. Alex has 2 water already (collected at T+8 and T+13). After Food Grove, I need to get 2 water (go to Water Source or meet Alex there), then both head to East Shelter by T+180. Current plan: MOVE to Central Camp now.

## M8  ·  seq 27  ·  T+26  ·  Alex → Sam
MESSAGE: "Sam, heading to Food Grove now. Should arrive around T+63. See you there!"
TRUE STATE: Alex at north_ridge with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE rock_field  ·  NEXT: T+36 MOVE central_camp, T+48 MOVE east_shelter, T+66 MOVE food_grove, T+81 COLLECT food
NOTE (verbatim): At T+26, North Ridge. I have 2 water. Sam said at T+20 he's heading to Food Grove. My plan is still on track: Rock Field (10min) -> Central Camp (12min) -> Food Grove (15min) = 37min total = T+63. Sam should arrive Food Grove around T+35 (he left South Beach at T+0, goes South Beach->Central Camp 20min->Food Grove 15min = T+35). At Food Grove we'll collect food together, then head to East Shelter (15min) = T+78. Plenty of time before T+180. The bridge to Food Grove is broken so can't cross from South Beach - but Sam is going via Central Camp so that's fine. Continuing to Food Grove now.

## M9  ·  seq 31  ·  T+36  ·  Alex → Sam
MESSAGE: "Sam, at Rock Field now heading to Central Camp then Food Grove. Should be there by T+63. See you soon!"
TRUE STATE: Alex at rock_field with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+48 MOVE east_shelter, T+66 MOVE food_grove, T+81 COLLECT food, T+86 COLLECT food
NOTE (verbatim): At T+36 at Rock Field with 2 water. Sam said he'd be at Food Grove around T+35, so he should be there or arriving now. My plan: Rock Field->Central Camp (12min, T+48)->Food Grove (15min, T+63). Sam should already be at Food Grove collecting food. Need to meet him there, collect food together, then head to East Shelter (15min from Food Grove = T+78). Still well ahead of T+180 deadline. Moving to Central Camp now.

## M10  ·  seq 35  ·  T+40  ·  Sam → Alex
MESSAGE: "Heading to Food Grove now via East Shelter route. Will collect food and wait for you there!"
TRUE STATE: Sam at central_camp with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+58 MOVE food_grove, T+73 COLLECT food, T+78 WAIT 10, T+88 COLLECT food
NOTE (verbatim): T+40 at Central Camp. Alex said at T+36 they're at Rock Field heading to Central Camp then Food Grove, should arrive T+63. I need to get to Food Grove to collect 2 food. From Central Camp to Food Grove is 15 min, so I'll arrive T+55. Alex should arrive around T+63. After Food Grove, I need 2 water - I can either go to Water Source (8+8=16 min from Food Grove via North Ridge+Water Source) or wait for Alex who already has 2 water. Plan: Move to Food Grove now (15 min, arrive T+55), collect food, wait for Alex, then figure out water strategy. We have 140 min until rescue at T+180. East Shelter from Food Grove is 15 min. So if we leave Food Grove at T+75, we arrive East Shelter at T+90, giving us 90 min buffer. This should work.

## M11  ·  seq 39  ·  T+48  ·  Alex → Sam
MESSAGE: "Sam, at Central Camp heading to Food Grove now. Should arrive T+63. See you there!"
TRUE STATE: Alex at central_camp with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+66 MOVE food_grove, T+81 COLLECT food, T+86 COLLECT food, T+91 MOVE east_shelter
NOTE (verbatim): At T+48 at Central Camp with 2 water, 0 food. Sam's last message (T+40) says he's heading to Food Grove via East Shelter route and will collect food and wait there. My plan: Central Camp->Food Grove (15min, T+63). Sam should be at Food Grove by then with food. We'll collect food together, then both head to East Shelter (15min, T+78). This gives us 102 minutes before rescue at T+180. We both need 2 food & 2 water. Sam is collecting food, I have 2 water. Timeline looks good. Moving to Food Grove now.

## M12  ·  seq 43  ·  T+58  ·  Sam → Alex
MESSAGE: "Alex, I'm at East Shelter heading to Food Grove now. Should arrive T+73. Let's meet there!"
TRUE STATE: Sam at east_shelter with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+73 COLLECT food, T+78 WAIT 10, T+88 COLLECT food, T+93 MOVE east_shelter
NOTE (verbatim): At T+58, I'm at East Shelter with 0 food and 0 water. This is wrong - I should have gone to Food Grove to collect food! My last message at T+40 said I was heading to Food Grove via East Shelter route, but I ended up at East Shelter instead. I need to correct course immediately. Alex's last message (T+48) said they're at Central Camp heading to Food Grove, should arrive T+63. I need to: 1) Go to Food Grove immediately (15 min, arrive T+73), 2) Collect food there, 3) Wait for Alex or coordinate with them, 4) Get 2 water (either from Alex or Water Source), 5) Both reach East Shelter by T+180. Current plan: Move to Food Grove now. This takes 15 min, arriving T+73. Alex should be there or arriving soon. We can collect food together, then figure out water. We have 107 min left after arriving at Food Grove - plenty of time to get water and reach East Shelter (15 min from Food Grove to East Shelter).

## M13  ·  seq 47  ·  T+66  ·  Alex → Sam
MESSAGE: "Sam, I'm at East Shelter heading to Food Grove now. Should arrive T+81. See you there!"
TRUE STATE: Alex at east_shelter with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+81 COLLECT food, T+86 COLLECT food, T+91 MOVE east_shelter, T+106 WAIT 30
NOTE (verbatim): At T+66 at East Shelter with 2 water, 0 food. Sam's last message (T+58) says he's at East Shelter heading to Food Grove, should arrive T+73. I'm currently AT East Shelter - Sam may already be here or arriving very soon. I need to check Food Grove to meet Sam there. My plan: go to Food Grove now (15min, arrive T+81). Sam should be there or arriving around T+73. Once we meet at Food Grove, we'll collect food together, then both return to East Shelter (15min, T+96). This gives us 84 minutes buffer before T+180 rescue. We both need 2 food & 2 water. I have 2 water, Sam is collecting food.

## M14  ·  seq 51  ·  T+73  ·  Sam → Alex
MESSAGE: "Alex, I'm at Food Grove collecting food now. You should arrive soon. We'll get water together after you arrive."
TRUE STATE: Sam at food_grove with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove had 6 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+78 WAIT 10, T+88 COLLECT food, T+93 MOVE east_shelter, T+108 MOVE central_camp
NOTE (verbatim): At T+73, I'm at Food Grove with 0 food and 0 water. Alex's last message (T+66) said they're at East Shelter heading to Food Grove, should arrive T+81. I need to: 1) COLLECT food now (5 min, T+78), 2) Wait for Alex to arrive (T+81), 3) Then we both need to get 2 water each. We have 107 min left. After collecting food here, I'll have 1 food. Alex should arrive T+81 with 2 water. We can collect more food together, then go get water from Water Source (8 min from North Ridge). Total time needed: collect food here (5 min), wait for Alex (8 min), collect more food if needed, travel to Water Source area (variable), get water, return to East Shelter (15 min from Food Grove). With 107 min available, this is tight but doable. Priority: collect food now.

## M15  ·  seq 54  ·  T+78  ·  Sam → Alex
MESSAGE: "Alex, at Food Grove with 1 food. Waiting for you. We'll collect more food here, then head to Water Source for water together."
TRUE STATE: Sam at food_grove with food 1, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove had 5 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+88 COLLECT food, T+93 MOVE east_shelter, T+108 MOVE central_camp, T+126 MOVE east_shelter
NOTE (verbatim): At T+78, I'm at Food Grove with 1 food, 0 water. Alex said they'd arrive T+81 (3 min away). I just collected food (T+73-T+78). Now I should WAIT for Alex to arrive. We have 102 min left. Once Alex arrives with their 2 water, we need: 1 more food each (2 total), then get water from Water Source. Alex has 2 water already, I need 2 water. Plan: Wait for Alex (arrive ~T+81), collect remaining food here if available, travel to Water Source area to collect water (8 min from North Ridge), return to East Shelter (15 min from Food Grove). Total: ~10 min wait + travel + collection + 15 min return = should fit in 102 min. WAIT 10 to let Alex arrive.

## M16  ·  seq 58  ·  T+81  ·  Alex → Sam
MESSAGE: "Sam, collecting food now. Let's each grab 2 more so we have 4 total, then head to East Shelter."
TRUE STATE: Alex at food_grove with food 0, water 2; Sam at food_grove with food 1, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove had 5 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+86 COLLECT food, T+91 MOVE east_shelter, T+106 WAIT 30, T+136 MOVE central_camp
NOTE (verbatim): T+81 at Food Grove with Sam. I have 2 water, 0 food. Sam has 1 food. We need 2 food & 2 water each for rescue (4 food, 4 water total). Food Grove has 5 food available. Plan: COLLECT food now (5 min, T+86), then Sam collects (T+91), then I collect again (T+96), then Sam collects (T+101). This gets us to 4 food total. Then MOVE to East Shelter (15 min, T+116) with 64 min buffer before T+180 rescue. Sam already has 2 water from earlier trips or can get from Water Source. We're in good shape.

## M17  ·  seq 61  ·  T+86  ·  Alex → Sam
MESSAGE: "Collecting food now. After this I'll have 2 food. Your turn to collect next so you get to 2 food. Then we both head to East Shelter."
TRUE STATE: Alex at food_grove with food 1, water 2; Sam at food_grove with food 1, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove had 4 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+91 MOVE east_shelter, T+106 WAIT 30, T+136 MOVE central_camp, T+154 MOVE east_shelter
NOTE (verbatim): T+86 at Food Grove. Current inventory: 1 food, 2 water. Sam is here with me. Food Grove has 4 food available. My last plan was to collect food alternately, but I need to reassess: I have 1 food (need 2), Sam has 1 food (needs 2). We need 4 food total, 4 water total. I have 2 water already. Sam said he'd get water together - he may have water or may not. Let me collect food now (T+91), then I'll have 2 food. Then Sam should collect to get to 2 food. Then we both need to ensure we have 2 water each. After food collection, we move to East Shelter (15 min) to arrive by T+116, leaving 64 min buffer. Proceeding with food collection.

## M18  ·  seq 64  ·  T+88  ·  Sam → Alex
MESSAGE: "Got it, collecting food now. After this we need to figure out water - we need 2 water each but time is tight. Let's discuss after I collect."
TRUE STATE: Sam at food_grove with food 1, water 0; Alex at food_grove with food 2, water 2
KNOWS: Water Source has water (unlimited). | Food Grove had 3 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+93 MOVE east_shelter, T+108 MOVE central_camp, T+126 MOVE east_shelter, T+144 WAIT 10
NOTE (verbatim): T+88: Alex is here at Food Grove. Alex has 2 food now. I have 1 food, 0 water. Alex wants me to collect food next so I get to 2 food. Then we both head to East Shelter. Plan: COLLECT food (5 min, T+93), then MOVE east_shelter (15 min, T+108). At East Shelter we still need 2 water each. Water Source is 8 min from North Ridge. From East Shelter: 18 min to Central Camp, 12 min to Rock Field, 10 min to North Ridge, 8 min to Water Source = 48 min total. Then 48 min back = 96 min. Total time: 5 + 15 + 48 + 48 = 116 min. We have 92 min left. This won't work! Alternative: We need to get water BEFORE East Shelter. From Food Grove: go to Central Camp (via East Shelter 15 min back + 18 min = 33 min OR via South Beach 10 min + 20 min = 30 min), then North Ridge (12 min), then Water Source (8 min). Total: 30 + 12 + 8 = 50 min. Then back to East Shelter: Water Source to North Ridge (8 min), North Ridge to Rock Field (10 min), Rock Field to Central Camp (12 min), Central Camp to East Shelter (18 min) = 48 min. Grand total: 5 (collect) + 50 (to water) + 48 (back) = 103 min. We have 92 min. Still too tight! Wait - bridge is broken so can't use South Beach route easily. Let me recalculate: From Food Grove, go to East Shelter (15 min), then Central Camp (18 min), then North Ridge (12 min), then Water Source (8 min) = 53 min. Back: Water Source to North Ridge (8 min), to Rock Field (10 min), to Central Camp (12 min), to East Shelter (18 min) = 48 min. Total: 5 + 53 + 48 = 106 min. Still over 92 min. We're in trouble. Let me collect food first as Alex requested, then reassess.

## M19  ·  seq 69  ·  T+93  ·  Sam → Alex
MESSAGE: "Alex, moving to East Shelter now. We need water urgently - time is tight. Meet me there or let me know where you are."
TRUE STATE: Sam at food_grove with food 2, water 0; Alex at travelling with food 2, water 2
KNOWS: Water Source has water (unlimited). | Food Grove had 2 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+108 MOVE central_camp, T+126 MOVE east_shelter, T+144 WAIT 10, T+154 WAIT 10
NOTE (verbatim): T+93: I have 2 food, 0 water. Alex should be at or near Food Grove with 2 food. We need 2 water each to be rescued. Time left: 87 min. Critical path: Get water first, then to East Shelter. From Food Grove to Water Source: 15 min to East Shelter, 18 min to Central Camp, 12 min to North Ridge, 8 min to Water Source = 53 min. Collect 2 water (10 min). Return to East Shelter: 8+10+12+18 = 48 min. Total: 53+10+48 = 111 min. We only have 87 min left - WE CANNOT MAKE IT! We need a faster route. Wait - I can go: Food Grove to South Beach (10 min via bridge... but bridge is broken). Alternative: Food Grove to Central Camp (via East Shelter back 15 min + 18 min = 33 min, OR the long way). Actually, shortest from Food Grove to Water Source without using broken bridge: Food Grove -> East Shelter (15) -> Central Camp (18) -> North Ridge (12) -> Water Source (8) = 53 min. This is too slow. CRITICAL REALIZATION: We might not have enough time. But we must try. Move to East Shelter first (15 min), then assess if we can do water run. Or wait for Alex here and coordinate. Let me move to East Shelter to position closer to water source.

## M20  ·  seq 76  ·  T+108  ·  Sam → Alex
MESSAGE: "Alex, do you have water? We need 2 each for rescue. Time is critical - 72 min left. What's your status?"
TRUE STATE: Sam at east_shelter with food 2, water 0; Alex at east_shelter with food 2, water 2
KNOWS: Water Source has water (unlimited). | Food Grove had 2 food left (you were last there at T+93). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+126 MOVE east_shelter, T+144 WAIT 10, T+154 WAIT 10, T+164 WAIT 10
NOTE (verbatim): T+108: CRITICAL SITUATION. I'm at East Shelter with Alex. I have 2 food, 0 water. Alex is here - need to check his inventory. We have 72 min until rescue at T+180. MUST GET 2 WATER EACH. Fastest water route from East Shelter: East Shelter -> Central Camp (18) -> North Ridge (12) -> Water Source (8) = 38 min to reach water. Collect 2 water (10 min) = 48 min total. Return: 8+12+18 = 38 min. Total: 48+38 = 86 min. We'd arrive at T+194 - TOO LATE by 14 min! PROBLEM: We cannot make it if we both go for water together. SOLUTION: One of us gets water while other waits at East Shelter. I should go get 2 water now (86 min round trip would put me back at T+194, but Alex can stay here and we meet at East Shelter). Wait - that's still too late. ALTERNATIVE: Can we get water faster? No faster route exists. We are in serious trouble. Let me go to Central Camp first and reassess - maybe Alex has water already? Ask Alex immediately about his water status.
