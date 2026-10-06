# Evidence — L2-C (Level 2 Split Knowledge)

## M1  ·  seq 1  ·  T+0  ·  Alex → Sam
MESSAGE: "Sam, this is Alex. Starting at North Ridge, heading to Water Source. Need to meet up and get supplies for rescue at East Shelter by T+180."
TRUE STATE: Alex at north_ridge with food 0, water 0; Sam at south_beach with food 0, water 0
KNOWS: Water Source has water (unlimited). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE water_source  ·  NEXT: T+8 COLLECT water, T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field
NOTE (verbatim): T+0 at North Ridge. Need to: 1) Find Sam, 2) Gather 2 food + 2 water each, 3) Both reach East Shelter by T+180. Water Source is 8 min away - good first move to secure water. Then need to find Sam and coordinate gathering food. Food Grove is accessible from East Shelter (15 min). Shipwreck area also has Food Grove nearby. Total time budget: 180 min. Strategy: Get water first, then search for Sam while gathering food.

## M2  ·  seq 2  ·  T+0  ·  Sam → Alex
MESSAGE: "Hi Alex! I'm at South Beach heading to Food Grove to get food. Meet me there if you can!"
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at north_ridge with food 0, water 0
KNOWS: Food Grove has food.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+10 WAIT 10, T+20 MOVE shipwreck, T+30 MOVE south_beach, T+40 MOVE central_camp
NOTE (verbatim): Starting at South Beach at T+0. Need to reach East Shelter by T+180 with Alex, both carrying 2+ food and 2+ water. Food Grove is 10 min away via bridge. Should gather food first, then water, then coordinate with Alex. Total travel time to East Shelter from South Beach: South Beach -> Food Grove (10 min) -> East Shelter (15 min) = 25 min. Need to find Alex and ensure we both have supplies.

## M3  ·  seq 9  ·  T+8  ·  Alex → Sam
MESSAGE: "At Water Source now, collecting water. Saw your message - heading to South Beach to meet you. Bridge is broken so Food Grove access limited. Will coordinate there. ETA soon."
TRUE STATE: Alex at water_source with food 0, water 0; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp
NOTE (verbatim): T+8 at Water Source. Sam is at South Beach heading to Food Grove. The bridge between South Beach and Food Grove is broken, so Sam cannot cross there. Sam likely meant they're going to Food Grove via another route OR they're stuck at South Beach. I need to: 1) Collect water here (5 min), 2) Head to South Beach to find Sam (need to go north_ridge->central_camp->south_beach = 8+15+20=43 min), 3) Coordinate getting to Food Grove and gathering food, 4) Both reach East Shelter by T+180. After collecting water (T+13), I'll have 167 min left. Travel to South Beach (43 min) = T+56. Then figure out food gathering with Sam. Food Grove is 10 min from South Beach (via shipwreck area presumably, or 15 min from East Shelter). Need to secure 2 food + 2 water each = 4 food, 4 water total. Priority: collect water now, find Sam, coordinate food gathering.

## M4  ·  seq 14  ·  T+10  ·  Sam → Alex
MESSAGE: "Alex, I'm at South Beach. Bridge to Food Grove is broken. Where are you? Let's meet up and figure out supplies together."
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at water_source with food 0, water 1
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+20 MOVE shipwreck, T+30 MOVE south_beach, T+40 MOVE central_camp, T+60 MOVE east_shelter
NOTE (verbatim): At T+10, South Beach. Alex is heading to South Beach from Water Source (started at North Ridge, went to Water Source at T+0, collected water, now en route). Alex's message at T+8 said 'heading to South Beach to meet you. ETA soon' - so Alex should arrive soon. Bridge to Food Grove is broken, so that route is blocked. Need to find alternative food source. Shipwreck is 10 min away (might have supplies). Central Camp is 20 min away. Alex said they collected water at Water Source. I have 0 food, 0 water. PLAN: Wait for Alex to arrive at South Beach, then figure out food source together. Shipwreck might have supplies. After getting supplies, need to reach East Shelter by T+180 with 2+ food and 2+ water each. Current time budget: 170 min remaining. South Beach to East Shelter: South Beach -> Central Camp (20 min) -> East Shelter (18 min) = 38 min travel. So I have 132 min to gather supplies before needing to leave. WAIT 10 to see if Alex arrives.

## M5  ·  seq 17  ·  T+13  ·  Alex → Sam
MESSAGE: "Sam, at Water Source collecting water. Heading to South Beach now - ETA T+61. We'll figure out food access together. Stay put."
TRUE STATE: Alex at water_source with food 0, water 1; Sam at south_beach with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 WAIT 10
NOTE (verbatim): T+13 at Water Source with 1 water. Sam is at South Beach (confirmed at T+10). I have 167 min until rescue. Plan: 1) Collect water here now (5 min, T+18), then 2) Travel to South Beach via north_ridge->central_camp->south_beach (8+15+20=43 min, arrive T+61). 3) At South Beach with Sam, we need to find food. Food Grove is accessible from South Beach but bridge is broken - must go around via shipwreck or another route. 4) Need 4 food + 4 water total for both of us to be rescued. After reaching South Beach at T+61, I'll have 119 min left. Food Grove trip + gathering should take ~30-40 min, then travel to East Shelter (18 min from Central Camp). Timeline is tight but doable. Collecting water now.

## M6  ·  seq 20  ·  T+18  ·  Alex → Sam
MESSAGE: "Sam, heading to South Beach now. ETA T+61. Let's coordinate food gathering there."
TRUE STATE: Alex at water_source with food 0, water 2; Sam at south_beach with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE north_ridge  ·  NEXT: T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 WAIT 10, T+58 WAIT 10
NOTE (verbatim): T+18 at Water Source with 2 water. Sam was at South Beach at T+10, heading there to meet. Plan: Travel to South Beach via north_ridge->central_camp->south_beach (8+15+20=43 min, arrive T+61). Then coordinate with Sam to find food. We need 4 food + 4 water total for rescue. Food Grove is inaccessible via bridge from South Beach, but may be reachable from another route. After South Beach, have 119 min to get food and reach East Shelter (18 min from Central Camp). Timeline tight but feasible. Starting journey now.

## M7  ·  seq 23  ·  T+20  ·  Sam → Alex
MESSAGE: "Heading to Shipwreck to scout for food supplies. Should be back before you arrive. See you soon!"
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE shipwreck  ·  NEXT: T+30 MOVE south_beach, T+40 MOVE central_camp, T+60 MOVE east_shelter, T+78 MOVE food_grove
NOTE (verbatim): At T+20, South Beach. Alex said ETA T+61 to South Beach (41 min from now). I have 0 food, 0 water. Current plan: Alex is bringing water from Water Source. I need to find food. Options: (1) Wait for Alex at South Beach (ETA T+61), then explore Shipwreck together for supplies. (2) Go to Shipwreck now (10 min) to scout for food, return to South Beach by T+61. Shipwreck is 10 min away, so I could go there, spend some time exploring, and be back by T+50-60. This gives us time to coordinate. Timeline: MOVE shipwreck now (arrive T+30), explore 20-30 min, return to South Beach by T+50-60, meet Alex at T+61. Then we have 119 min to get supplies and reach East Shelter by T+180. South Beach -> Central Camp (20) -> East Shelter (18) = 38 min. So 81 min for gathering supplies. Should be enough if Shipwreck or another location has food. Going to Shipwreck now to scout.

## M8  ·  seq 27  ·  T+26  ·  Alex → Sam
MESSAGE: "Sam, heading to Shipwreck to meet you. ETA T+89. What food did you find? We need 4 total."
TRUE STATE: Alex at north_ridge with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE rock_field  ·  NEXT: T+36 MOVE central_camp, T+48 WAIT 10, T+58 WAIT 10, T+68 MOVE east_shelter
NOTE (verbatim): T+26 at North Ridge with 2 water. Sam was at South Beach at T+10, then headed to Shipwreck at T+20 to scout for food. My plan was to reach South Beach by T+61, but Sam is now at Shipwreck. I need to recalculate: From North Ridge to Shipwreck is north_ridge->central_camp->south_beach->shipwreck (15+18+20+10=63 min, arrive T+89). That's still feasible - leaves 91 min to gather food and reach East Shelter (18 min from Central Camp). Critical path: 1) Get to Shipwreck to meet Sam, 2) Gather 4 food total, 3) Reach East Shelter by T+180. Food Grove is blocked by broken bridge from South Beach, but may be accessible from other routes (need to explore). Continue toward South Beach/Shipwreck to meet Sam and coordinate food gathering.

## M9  ·  seq 31  ·  T+30  ·  Sam → Alex
MESSAGE: "Alex, heading back to South Beach now. Plan: go South Beach->Central Camp->Food Grove to get food. Meet me at Food Grove or South Beach. We need supplies ASAP."
TRUE STATE: Sam at shipwreck with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE south_beach  ·  NEXT: T+40 MOVE central_camp, T+60 MOVE east_shelter, T+78 MOVE food_grove, T+93 COLLECT food
NOTE (verbatim): At T+30, at Shipwreck. Alex is heading here with ETA T+89 - they're bringing water from Water Source. I have 0 food, 0 water still. The bridge to Food Grove is broken so I can't access it directly from South Beach. Need to find food elsewhere. Alex says they need 4 total food. My options: (1) WAIT here for Alex (they arrive T+89), but that's 59 min of waiting - wasteful. (2) MOVE back to South Beach (10 min, arrive T+40), then figure out how to reach Food Grove. Food Grove is accessible from Central Camp (12 min from Rock Field, or 15 min from West Forest). The path is: South Beach -> Central Camp (20 min) -> Food Grove (15 min) = 35 min total. Or I could go back to South Beach and then Central Camp -> Food Grove. Let me move back to South Beach now and regroup. If I go South Beach -> Central Camp -> Food Grove, I arrive at T+40+20+15=T+75. Alex arrives Shipwreck at T+89. I should be at Food Grove by T+75 gathering food. Alex will come to Shipwreck at T+89 and realize I'm not there - they'll need to find me or I'll need to coordinate. Better: move back to South Beach now, send Alex a message about the plan to reach Food Grove via Central Camp.

## M10  ·  seq 35  ·  T+36  ·  Alex → Sam
MESSAGE: "Sam, I'm at Rock Field heading to Central Camp. Food Grove is blocked from South Beach by broken bridge - need to find alternate route or food source. Meet me at Central Camp to coordinate. ETA T+48."
TRUE STATE: Alex at rock_field with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+48 WAIT 10, T+58 WAIT 10, T+68 MOVE east_shelter, T+86 MOVE food_grove
NOTE (verbatim): T+36 at Rock Field with 2 water. Sam's last message (T+30) says heading back to South Beach, then plans to go South Beach->Central Camp->Food Grove. But Food Grove is blocked from South Beach by broken bridge! Sam may not realize this. I need to intercept Sam and clarify the situation. From Rock Field: rock_field->central_camp is 12 min (arrive T+48). From Central Camp I can reach South Beach (18 min, T+66) or go directly toward Food Grove. Actually, Sam said 'South Beach->Central Camp->Food Grove' - maybe Sam thinks there's another route? Or Sam is confused about bridge status. I should go to Central Camp (12 min) to intercept Sam on the way, or continue to South Beach (30 min total from here: 12+18) to meet Sam there. Central Camp is the hub - if Sam is going through there, I'll catch them. Moving to Central Camp now.

## M11  ·  seq 39  ·  T+40  ·  Sam → Alex
MESSAGE: "Alex, heading to Central Camp now, ETA T+60. Let's meet there and coordinate access to Food Grove together. We need to get 4 food total before reaching East Shelter."
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+60 MOVE east_shelter, T+78 MOVE food_grove, T+93 COLLECT food, T+98 COLLECT food
NOTE (verbatim): Alex is at Rock Field heading to Central Camp with ETA T+48. I'm at South Beach at T+40. Alex suggests meeting at Central Camp to coordinate. I have 0 food, 0 water. Alex is bringing water from Water Source. The bridge to Food Grove is broken from South Beach, so I need to go through Central Camp. Plan: MOVE to Central Camp (20 min, arrive T+60). Alex should be there by T+48, so they'll wait for me. Once together at Central Camp, we can access Food Grove (15 min away). We need 4 food total and 4 water total (2 each for rescue). After getting food, we need to reach East Shelter by T+180. Time check: T+60 (arrive Central Camp) + T+15 (to Food Grove) = T+75 gathering food. Then T+75 + travel back to Central Camp + T+18 to East Shelter = roughly T+108 at East Shelter. That gives us 72 minutes buffer before T+180 storm/rescue. This should work if we can find enough food at Food Grove.

## M12  ·  seq 43  ·  T+48  ·  Alex → Sam
MESSAGE: "Sam, I'm at Central Camp. Waiting for you here. We need to plan food access - remember the bridge is broken so South Beach->Food Grove won't work. Let's coordinate when you arrive."
TRUE STATE: Alex at central_camp with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+58 WAIT 10, T+68 MOVE east_shelter, T+86 MOVE food_grove, T+101 COLLECT food
NOTE (verbatim): T+48 at Central Camp. Sam's last message (T+40) says heading to Central Camp with ETA T+60, so Sam should arrive in about 12 minutes. I'm here early. I should WAIT 10 to see if Sam arrives, then reassess. Current inventory: 0 food, 2 water. We need 4 food and 4 water total (2 each) to be rescued. Key facts: (1) Bridge between South Beach and Food Grove is broken - cannot access Food Grove from South Beach. (2) Food Grove is accessible from East Shelter (15 min). (3) We have 132 minutes until rescue at East Shelter. Critical path: Get food somehow, then both reach East Shelter by T+180. Sam thinks we can get food at Food Grove via South Beach->Central Camp->Food Grove, but that won't work because of the broken bridge. We need to either: (a) Find food elsewhere (Shipwreck?), or (b) Go to Food Grove via East Shelter route. Waiting here gives Sam time to arrive so we can coordinate in person.

## M13  ·  seq 49  ·  T+60  ·  Sam → Alex
MESSAGE: "Alex, let's head to East Shelter now and secure our position. We can gather supplies on the way or nearby. We have 120 min before rescue - plenty of time."
TRUE STATE: Sam at central_camp with food 0, water 0; Alex at central_camp with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+78 MOVE food_grove, T+93 COLLECT food, T+98 COLLECT food, T+103 COLLECT food
NOTE (verbatim): T+60: I'm at Central Camp with Alex. Alex has water from Water Source. I have 0 food, 0 water. We need 4 food and 4 water total (2 each for rescue). From Central Camp, Food Grove is 15 min away. We can reach it, gather food, and return to Central Camp (T+60 + 15 + 15 = T+90). Then travel to East Shelter (18 min, arrive T+108). This gives us 72 min buffer before T+180. The plan is solid - go to Food Grove now with Alex to collect food. Alex should have water; I need to get food. Let's execute.

## M14  ·  seq 52  ·  T+68  ·  Alex → Sam
MESSAGE: "Sam, heading to East Shelter now. Meet me there so we can coordinate food gathering from Food Grove. We need to move fast."
TRUE STATE: Alex at central_camp with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+86 MOVE food_grove, T+101 COLLECT food, T+106 COLLECT food, T+111 MOVE east_shelter
NOTE (verbatim): T+68 at Central Camp. Sam's last message at T+60 said 'heading to East Shelter now' - but I don't know if Sam actually arrived there or is still en route. Sam was supposed to arrive at Central Camp by T+60, but didn't show up. This is concerning. Sam's plan to 'head to East Shelter now' suggests Sam may have bypassed Central Camp and gone directly there (Central Camp->East Shelter is 18 min, so Sam could arrive T+78). Alternatively, Sam is delayed or took a different route. Current inventory: 0 food, 2 water. We need 4 food and 4 water by T+180 (112 min left). CRITICAL ISSUE: We have NO FOOD yet and only 2 water. Food Grove is accessible via East Shelter route (East Shelter->Food Grove 15 min), but we haven't secured any food. Shipwreck was scouted by Sam but we don't know what's there. DECISION: I should move to East Shelter to (1) meet Sam if he's there, (2) position myself at the rescue location, (3) plan food gathering from Food Grove. This is 18 min. If Sam is at East Shelter, we can coordinate in person (saving messages). If not, I'll wait and search. Time is tight but this maximizes our chances. Moving to East Shelter now.

## M15  ·  seq 56  ·  T+78  ·  Sam → Alex
MESSAGE: "Alex, heading to Food Grove now to gather food. Meet me there or at East Shelter. We need to get 4 food total. ETA Food Grove T+93."
TRUE STATE: Sam at east_shelter with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+93 COLLECT food, T+98 COLLECT food, T+103 COLLECT food, T+108 MOVE east_shelter
NOTE (verbatim): T+78: I'm at East Shelter. Alex said they're heading here (last message T+68). I have 0 food, 0 water. Alex should have water from Water Source. We need 4 food total and 4 water total by T+180 (102 min left). Food Grove is 15 min away from East Shelter. If I go there now: T+78 + 15 = T+93 arrival. I can gather food and return T+93 + 15 = T+108 back at East Shelter. That's 72 min buffer - plenty of time. Alex might already be here or arriving soon. I should wait a bit to see if Alex shows up, then coordinate. Actually, let me go to Food Grove now to secure food while Alex either arrives here or meets me there. Food Grove is accessible from East Shelter (15 min path exists). Let's move.

## M16  ·  seq 60  ·  T+86  ·  Alex → Sam
MESSAGE: "Sam, heading to Food Grove now to meet you. ETA T+101. Let's gather food and head back to East Shelter together."
TRUE STATE: Alex at east_shelter with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+101 COLLECT food, T+106 COLLECT food, T+111 MOVE east_shelter, T+126 WAIT 30
NOTE (verbatim): T+86 at East Shelter. Sam's last message (T+78) says he's heading to Food Grove with ETA T+93 (7 min from now). Sam should arrive at Food Grove around T+93. I'm at East Shelter. Food Grove is 15 min away from East Shelter. If I move to Food Grove now, I'll arrive at T+101. Sam should be there by then (or shortly after). This is our best chance to coordinate and gather food together. We still need 4 food and 2 more water. After gathering food at Food Grove, we can return to East Shelter together with supplies. We have 94 min left - tight but doable if we act now. Moving to Food Grove to meet Sam.

## M17  ·  seq 64  ·  T+93  ·  Sam → Alex
MESSAGE: "At Food Grove now, collecting food. You're 8 min away, ETA T+101. Let's gather supplies here and head to East Shelter together."
TRUE STATE: Sam at food_grove with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove had 6 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+98 COLLECT food, T+103 COLLECT food, T+108 MOVE east_shelter, T+123 WAIT 10
NOTE (verbatim): T+93 at Food Grove. Alex ETA T+101 here (8 min away). I have 0 food, 0 water. Need 4 food and 4 water total by T+180 (87 min left). Alex has water from Water Source. Plan: COLLECT food now (5 min, done by T+98), then wait for Alex to arrive (T+101). We'll gather enough food here, then return to East Shelter together with time to spare. Food Grove has 6 food available - should be enough. After collecting, I'll have time to gather more if needed before heading back.

## M18  ·  seq 67  ·  T+98  ·  Sam → Alex
MESSAGE: "Collecting more food now. You're almost here - ETA T+101. Let's gather what we need and head to East Shelter together."
TRUE STATE: Sam at food_grove with food 1, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove had 5 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+103 COLLECT food, T+108 MOVE east_shelter, T+123 WAIT 10, T+133 WAIT 10
NOTE (verbatim): T+98 at Food Grove. I have 1 food, 0 water. Alex ETA T+101 (3 min away). I just collected once, need to collect again to get more food. Food Grove has 5 food available total - I've taken 1, so 4 remain. Need 4 food and 4 water total by T+180 (82 min left). Alex has water from Water Source. Plan: COLLECT food again (5 min, done by T+103). This will give me 2 food. Then wait for Alex (arrives T+101, will be here by T+103). Once Alex arrives, we collect remaining food together, then head to East Shelter (15 min). Timeline: T+103 I'll have 2 food after second collect. Alex arrives T+101 with water. We can collect more food together. Then travel to East Shelter T+118. That gives us 62 min buffer before T+180. Should be enough time.

## M19  ·  seq 71  ·  T+101  ·  Alex → Sam
MESSAGE: "Collecting food now. How much do you have? Let's gather what we need and head to East Shelter soon."
TRUE STATE: Alex at food_grove with food 0, water 2; Sam at food_grove with food 2, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove had 4 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+106 COLLECT food, T+111 MOVE east_shelter, T+126 WAIT 30, T+156 WAIT 10
NOTE (verbatim): T+101 at Food Grove with Sam. We have 79 min until rescue at T+180. Current inventory: 0 food, 2 water. Sam is here. We need 4 food total and 2 water each (4 water total). Sam should have collected some food already. I need to: 1) COLLECT food here (5 min) to get what's available, 2) Check Sam's inventory via GIVE water action or by collecting, 3) Get back to East Shelter with 2 food and 2 water each. Timeline: COLLECT food (T+106), then assess what we have. Food Grove had 4 food available. If I collect now, I should get some. Then move to East Shelter (15 min, T+121). That gives us 59 min buffer before T+180. Sam may already have food from earlier collections. Let's collect food now to maximize our supplies.

## M20  ·  seq 74  ·  T+103  ·  Sam → Alex
MESSAGE: "Alex, collect what you can here. I'm getting the last food. Then we head to East Shelter. Do you have water to share?"
TRUE STATE: Sam at food_grove with food 2, water 0; Alex at food_grove with food 1, water 2
KNOWS: Food Grove had 3 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+108 MOVE east_shelter, T+123 WAIT 10, T+133 WAIT 10, T+143 GIVE food
NOTE (verbatim): T+103 at Food Grove with Alex. I have 2 food, 0 water. Alex just arrived and is collecting food. Food Grove had 3 food left when I arrived - I collected 2, so 1 should remain (or Alex might have collected it). Critical issue: I have NO WATER and need 2 water by T+180 to be rescued. We need 4 food total and 4 water total (2 each). Alex has water from Water Source. Timeline: T+103 now, T+180 rescue = 77 min left. East Shelter is 15 min away. If we leave now (T+103), we arrive T+118, giving 62 min buffer. But I MUST get water. Options: (1) Collect remaining food here, (2) Get water somehow. Water Source is far (would need to backtrack through Central Camp, Rock Field, North Ridge = 12+10+8 = 30 min each way = 60 min total, leaving only 17 min). BEST PLAN: Collect the last food here (5 min, done T+108). Then move to East Shelter (15 min, arrive T+123). That's 57 min before rescue. Ask Alex about water - he should have some from Water Source. We can figure out water sharing at East Shelter. Let's secure position first.
