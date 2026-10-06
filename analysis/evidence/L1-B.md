# Evidence — L1-B (Level 1 Baseline)

## M1  ·  seq 1  ·  T+0  ·  Alex → Sam
MESSAGE: "Sam, I'm at North Ridge heading to Water Source. Need to meet up and gather supplies for East Shelter by T+180."
TRUE STATE: Alex at north_ridge with food 0, water 0; Sam at south_beach with food 0, water 0
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE water_source  ·  NEXT: T+8 COLLECT water, T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field
NOTE (verbatim): At T+0, starting at North Ridge with no supplies. Need to: 1) Find Sam, 2) Gather 2 food and 2 water each (4 total), 3) Both reach East Shelter by T+180. Water Source is 8min away (north_ridge->water_source). Food Grove requires going through central_camp and either east_shelter or south_beach. Bridge to Food Grove is broken so must use south_beach route: north_ridge->rock_field->central_camp->south_beach->food_grove (12+12+20+10=54min) OR north_ridge->rock_field->central_camp->east_shelter->food_grove (12+12+18+15=57min). Fastest water path: 8min. Fastest food path via south_beach: 54min. Total minimum: 62min for supplies + travel to East Shelter. Must find Sam soon. Starting with water since it's closest and critical.

## M2  ·  seq 2  ·  T+0  ·  Sam → Alex
MESSAGE: "Hi Alex, I'm at South Beach heading to Shipwreck to explore. Where are you?"
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at north_ridge with food 0, water 0
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE shipwreck  ·  NEXT: T+10 MOVE south_beach, T+20 WAIT 10, T+30 MOVE central_camp, T+50 MOVE east_shelter
NOTE (verbatim): Starting at South Beach at T+0. Need to reach East Shelter by T+180 with Alex, both carrying 2+ food and 2+ water to be rescued. Bridge to Food Grove is broken so can't use that route. Must explore to find Alex and gather supplies. Shipwreck might have supplies or info about Alex. Central Camp is a hub location - good for meeting up.

## M3  ·  seq 9  ·  T+8  ·  Alex → Sam
MESSAGE: "Sam, I'm at Water Source collecting water. Don't stay at Shipwreck long - meet me at South Beach to gather food together. I'll head there next."
TRUE STATE: Alex at water_source with food 0, water 0; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp
NOTE (verbatim): T+8: At Water Source. Sam is at South Beach heading to Shipwreck - that's concerning since Shipwreck is a dead end. I need to collect water now (5min, T+13), then head to intercept Sam. Sam's route: South Beach->Shipwreck is 10min, so Sam will be at Shipwreck around T+10. I should collect water, then move north_ridge (8min, T+21), then figure out how to reach Sam. From north_ridge I can go rock_field->central_camp->south_beach (12+12+20=44min, T+65) to intercept. That gives me time. Need to tell Sam to wait or meet me. Actually, I should collect water first, THEN move and message Sam with a plan.

## M4  ·  seq 13  ·  T+10  ·  Sam → Alex
MESSAGE: "On my way to South Beach now. See you there soon!"
TRUE STATE: Sam at shipwreck with food 0, water 0; Alex at water_source with food 0, water 1
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE south_beach  ·  NEXT: T+20 WAIT 10, T+30 MOVE central_camp, T+50 MOVE east_shelter, T+68 MOVE food_grove
NOTE (verbatim): At Shipwreck T+10. Alex is at Water Source collecting water and will head to South Beach to gather food together. I need to head to South Beach to meet Alex there. Shipwreck has no supplies visible. Route: Shipwreck -> South Beach (10 min) arrives T+20. Alex said to meet at South Beach to gather food together. This aligns perfectly. After gathering supplies at South Beach/Food Grove area, we need to reach East Shelter by T+180 with 2+ food and 2+ water each. Still have 170 minutes. Plan: meet Alex at South Beach, gather food and water, then head to East Shelter together.

## M5  ·  seq 16  ·  T+13  ·  Alex → Sam
MESSAGE: "Great! I'm at Water Source collecting supplies. I'll head to South Beach to meet you - should be there around T+68. We'll gather food and head to East Shelter together for rescue."
TRUE STATE: Alex at water_source with food 0, water 1; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 MOVE east_shelter
NOTE (verbatim): T+13: At Water Source with 1 water. Sam said he's heading to South Beach (was at Shipwreck at T+10). I need 2 water and 2 food total for rescue. Current plan: collect water now (T+18), then move to meet Sam. From Water Source: north_ridge (8min, T+26) -> rock_field (10min, T+36) -> central_camp (12min, T+48) -> south_beach (20min, T+68). Sam should be at South Beach by then or shortly after. We can then go to Food Grove together. Food Grove is accessible from South Beach (10min direct path, since bridge is broken we need alternate: south_beach->central_camp->rock_field->north_ridge->west_forest->central_camp->food_grove is too long. Actually, re-reading map: Food Grove connects to East Shelter (15min) and South Beach (10min via bridge - but bridge is BROKEN). So from South Beach, I need: south_beach->central_camp->east_shelter->food_grove (18+15=33min) OR south_beach->shipwreck is dead end. Let me reconsider: south_beach->central_camp (20min) -> east_shelter (18min) -> food_grove (15min). That's 53min from South Beach. After collecting water at T+18, moving to south_beach at T+68, then to food_grove at T+121, then to east_shelter at T+136. That leaves 44min buffer before T+180. Should work. Collect water now.

## M6  ·  seq 19  ·  T+18  ·  Alex → Sam
MESSAGE: "Sam, heading to South Beach now - ETA around T+68. See you there!"
TRUE STATE: Alex at water_source with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE north_ridge  ·  NEXT: T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 MOVE east_shelter, T+66 WAIT 10
NOTE (verbatim): T+18: Good! I collected water at T+13 and now have 2 water total. My plan is still on track: head to South Beach to meet Sam, then go to Food Grove to collect food. Current inventory: 2 water, 0 food. I need 2 food to complete rescue requirements. Route: north_ridge (T+26) -> rock_field (T+36) -> central_camp (T+48) -> south_beach (T+68). Sam should be at/near South Beach by then. From South Beach, we go: central_camp (T+88) -> east_shelter (T+106) -> food_grove (T+121). That gives us 59 min buffer before T+180 to collect food and return to East Shelter. Moving to north_ridge now.

## M7  ·  seq 23  ·  T+20  ·  Sam → Alex
MESSAGE: "At South Beach now. Waiting for you. Bridge to Food Grove is broken - need to figure out supply route together."
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+30 MOVE central_camp, T+50 MOVE east_shelter, T+68 MOVE food_grove, T+83 COLLECT food
NOTE (verbatim): At South Beach T+20. Alex said ETA around T+68 to South Beach. I'm early and have 160 min until rescue at T+180. The bridge to Food Grove is broken so I can't cross there directly. I need to gather supplies before heading to East Shelter. Best plan: wait here for Alex at South Beach since they're coming here. We can then figure out how to get food and water. Food Grove is accessible via South Beach->Food Grove (10 min) but bridge is broken. Alternative: go to Central Camp and explore from there, or wait for Alex. Since Alex specifically said to meet at South Beach, I should wait. Let me wait 10 min and reassess.

## M8  ·  seq 27  ·  T+26  ·  Alex → Sam
MESSAGE: "Sam, bridge is broken! New plan: I'll go Central Camp -> East Shelter -> Food Grove instead. Meet me at East Shelter around T+66. We'll get food from Food Grove and return for rescue."
TRUE STATE: Alex at north_ridge with food 0, water 2; Sam at south_beach with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE rock_field  ·  NEXT: T+36 MOVE central_camp, T+48 MOVE east_shelter, T+66 WAIT 10, T+76 MOVE food_grove
NOTE (verbatim): T+26: Sam is at South Beach waiting for me. Critical problem: the bridge to Food Grove is broken! I can't use the route I planned (South Beach -> Food Grove via bridge). I need a new plan. Alternative route to Food Grove: Central Camp -> East Shelter -> Food Grove (15 min from East Shelter). New timeline: Continue to Rock Field (T+36) -> Central Camp (T+48) -> East Shelter (T+66) -> Food Grove (T+81). Collect 2 food, return to East Shelter by T+96. That gives 84 min buffer before T+180 - plenty of time. I need to inform Sam of the new plan since the bridge is broken. Current inventory: 2 water, 0 food. Proceeding to Rock Field now.

## M9  ·  seq 30  ·  T+30  ·  Sam → Alex
MESSAGE: "Got your message! Heading to Central Camp now, will meet you at East Shelter around T+68. Let's get food from Food Grove together."
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+50 MOVE east_shelter, T+68 MOVE food_grove, T+83 COLLECT food, T+88 COLLECT food
NOTE (verbatim): Alex's new plan at T+26: they're going Central Camp -> East Shelter -> Food Grove, ETA East Shelter around T+66. I should head to East Shelter to meet them there. From South Beach to East Shelter: South Beach -> Central Camp (20 min) -> East Shelter (18 min) = 38 min total. If I leave now at T+30, I'd arrive at T+68, which matches Alex's ETA of T+66 (close enough given travel time variability). This gives us time to get food from Food Grove and return to East Shelter before T+180 rescue. I have 0 food and 0 water currently - critical to gather supplies. Moving to Central Camp now.

## M10  ·  seq 34  ·  T+36  ·  Alex → Sam
MESSAGE: "On my way to Central Camp now. ETA T+48, then to East Shelter. See you there!"
TRUE STATE: Alex at rock_field with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+48 MOVE east_shelter, T+66 WAIT 10, T+76 MOVE food_grove, T+91 COLLECT food
NOTE (verbatim): T+36: I'm at Rock Field. Sam said he's heading to Central Camp to meet me at East Shelter around T+68. Perfect - we're on the same plan now. I need to continue to Central Camp (12 min, arrive T+48) -> East Shelter (18 min, arrive T+66) -> Food Grove (15 min, arrive T+81) to collect food, then return to East Shelter by T+96. This gives us 84 minutes buffer before rescue at T+180. Sam should arrive at East Shelter around T+68, so I'll be there waiting or just arriving. The plan is solid: both of us at East Shelter with 2+ food and 2+ water by T+96. Proceeding to Central Camp now.

## M11  ·  seq 38  ·  T+48  ·  Alex → Sam
MESSAGE: "Sam, I'm at Central Camp heading to East Shelter now, ETA T+66. See you around T+68!"
TRUE STATE: Alex at central_camp with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+66 WAIT 10, T+76 MOVE food_grove, T+91 COLLECT food, T+96 COLLECT food
NOTE (verbatim): T+48: I'm at Central Camp as planned. I have 2 water, 0 food. Sam said he'd meet me at East Shelter around T+68. I need to: 1) Go to East Shelter (18 min, arrive T+66) 2) Wait for Sam to arrive around T+68 3) Go to Food Grove together (15 min, arrive T+83) 4) Return to East Shelter (15 min, arrive T+98) - gives us 82 min buffer before T+180 rescue. The bridge is broken so we must go East Shelter -> Food Grove -> East Shelter. Proceeding to East Shelter now.

## M12  ·  seq 42  ·  T+50  ·  Sam → Alex
MESSAGE: "On my way to East Shelter now, should arrive around T+68. Let's meet there and plan our Food Grove trip!"
TRUE STATE: Sam at central_camp with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+68 MOVE food_grove, T+83 COLLECT food, T+88 COLLECT food, T+93 MOVE east_shelter
NOTE (verbatim): At T+50, at Central Camp. Alex said ETA T+66 at East Shelter. I should head to East Shelter now (18 min) to arrive around T+68, matching Alex's timeline. I have 0 food and 0 water - critical. Plan: meet Alex at East Shelter, then go to Food Grove together to gather supplies before returning for T+180 rescue. The broken bridge means we must access Food Grove via East Shelter (15 min from there). Total time check: T+68 at East Shelter + 15 min to Food Grove = T+83, plenty of time to gather food/water and return by T+180 (97 min buffer).

## M13  ·  seq 46  ·  T+66  ·  Alex → Sam
MESSAGE: "Sam, I'm at East Shelter. Waiting for you - should be here soon!"
TRUE STATE: Alex at east_shelter with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+76 MOVE food_grove, T+91 COLLECT food, T+96 COLLECT food, T+101 MOVE east_shelter
NOTE (verbatim): T+66: I'm at East Shelter as planned. Sam said he'd arrive around T+68, so I should wait for him. He's only 2 minutes behind schedule. I have 2 water, 0 food. Plan: Wait for Sam (he should arrive T+68), then together go to Food Grove (15 min, arrive T+83), return to East Shelter (15 min, arrive T+98). This gives us 82 minutes buffer before T+180 rescue. We both need 2 food and 2 water to be rescued. I have 2 water already; need 2 food. Sam needs to gather supplies too. Waiting 10 min to see if Sam arrives.

## M14  ·  seq 50  ·  T+68  ·  Sam → Alex
MESSAGE: "Alex! Let's head to Food Grove now and gather supplies. We need food and water before the rescue."
TRUE STATE: Sam at east_shelter with food 0, water 0; Alex at east_shelter with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+83 COLLECT food, T+88 COLLECT food, T+93 MOVE east_shelter, T+108 MOVE central_camp
NOTE (verbatim): Perfect! I'm at East Shelter at T+68 as planned, and Alex is here waiting. We both have 0 food and 0 water - critical supplies needed. Next step: go to Food Grove together (15 min, arriving T+83) to gather food and water. Then return to East Shelter for T+180 rescue. We have 97 minutes of buffer time, which is plenty. Moving to Food Grove now.

## M15  ·  seq 53  ·  T+76  ·  Alex → Sam
MESSAGE: "Sam, heading to Food Grove now! Meet me there or at East Shelter when done."
TRUE STATE: Alex at east_shelter with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+91 COLLECT food, T+96 COLLECT food, T+101 MOVE east_shelter, T+116 WAIT 30
NOTE (verbatim): T+76: Sam messaged at T+68 saying 'Let's head to Food Grove now' - he must be at East Shelter with me or very close. I need to move to Food Grove immediately to gather food. I have 2 water (good), 0 food (need 2). Sam needs supplies too. Food Grove is 15 min away (arrive T+91), then 15 min back to East Shelter (arrive T+106). This leaves 74 minutes buffer before T+180 rescue - plenty of time. Sam is likely waiting for me to move, or he's already heading there. Let's go.

## M16  ·  seq 57  ·  T+83  ·  Sam → Alex
MESSAGE: "At Food Grove collecting food now. How much have you gathered? We need 2 food + 2 water each for rescue."
TRUE STATE: Sam at food_grove with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove had 6 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+88 COLLECT food, T+93 MOVE east_shelter, T+108 MOVE central_camp, T+126 MOVE east_shelter
NOTE (verbatim): At T+83 in Food Grove. Alex said they're heading to Food Grove at T+76, so they should be here or arriving soon. I need to collect food first (5 min, done at T+88), then we both need to gather water before returning to East Shelter. Critical: we need at least 2 food and 2 water each to be rescued. Water Source is far (would need to go back through Central Camp), so I should focus on collecting all available food here first, then figure out water strategy. Alex might already be collecting or waiting. Let me collect food now.

## M17  ·  seq 60  ·  T+88  ·  Sam → Alex
MESSAGE: "Alex, still at Food Grove collecting. Have 1 food so far. Where are you? We need to coordinate water gathering soon."
TRUE STATE: Sam at food_grove with food 1, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove had 5 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+93 MOVE east_shelter, T+108 MOVE central_camp, T+126 MOVE east_shelter, T+144 WAIT 30
NOTE (verbatim): T+88: I just finished collecting 1 food (now have 1 food, 0 water). Food Grove had 5 food total - I need to collect more. Alex said they're heading to Food Grove at T+76, so they should be here or nearby. I haven't seen them yet. Critical timeline: T+180 is 92 min away. I need 2 food + 2 water for rescue. Strategy: (1) Collect remaining food here (4 more food available, takes 5 min each = 20 min total), (2) Get water from Water Source (16 min from here via East Shelter + Central Camp + North Ridge), (3) Return to East Shelter by T+180. If I collect all 5 food here (done by T+108), then go to Water Source (T+124), I can still make it back to East Shelter by T+180 with time to spare. But I need to find Alex - they should be collecting food too. Let me collect more food and message Alex.

## M18  ·  seq 64  ·  T+91  ·  Alex → Sam
MESSAGE: "Sam, collecting 2 food now. You need 1 more food + 2 water. After I collect, we head to East Shelter. Can you gather water on the way back?"
TRUE STATE: Alex at food_grove with food 0, water 2; Sam at food_grove with food 2, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove had 4 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+96 COLLECT food, T+101 MOVE east_shelter, T+116 WAIT 30, T+146 WAIT 10
NOTE (verbatim): T+91: I'm at Food Grove with Sam. He has 1 food, I have 0 food and 2 water. We both need 2 food + 2 water for rescue. Sam is still collecting. I need to collect food NOW - I can get 4 food total here (5 min per collection). After collecting, we head back to East Shelter (15 min). Timeline: T+91 COLLECT (T+96) -> COLLECT (T+101) -> MOVE east_shelter (T+116). This gives us 64 min buffer before T+180. Sam needs to gather water still - he has 0 water mentioned. We should coordinate: I'll collect 2 food here, he collects 1 more, then we both head to Water Source or back to East Shelter. Actually, wait - I need to be smarter. Sam has 1 food, needs 1 more. I have 0, need 2. Let me collect 2 food now, then we go to East Shelter where we can plan water gathering for Sam.

## M19  ·  seq 67  ·  T+93  ·  Sam → Alex
MESSAGE: "Alex, let's go to Water Source NOW to get water! We have enough food (2 each). East Shelter -> Central Camp -> North Ridge -> Water Source. No time to waste!"
TRUE STATE: Sam at food_grove with food 2, water 0; Alex at food_grove with food 1, water 2
KNOWS: Water Source has water (unlimited). | Food Grove had 3 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+108 MOVE central_camp, T+126 MOVE east_shelter, T+144 WAIT 30, T+174 WAIT 10
NOTE (verbatim): T+93: Great! Alex is here at Food Grove with me. I now have 2 food, Alex has 2 food. We both need 2 water each for rescue. Current plan: I should collect 1 more food here (5 min, done by T+98) to have buffer, then head to Water Source to get water. Water Source is: Food Grove -> East Shelter (15 min) -> Central Camp (18 min) -> North Ridge (10 min) -> Water Source (8 min) = 51 min total. If I leave at T+98, I arrive at Water Source at T+149, collect water (5 min, done T+154), then return: Water Source -> North Ridge (8 min) -> Central Camp (10 min) -> East Shelter (18 min) = 36 min = arrive T+190. That's too late! PROBLEM: I can't make it to Water Source and back in time. REVISED PLAN: Alex said they can gather water on the way back. Let me give Alex 1 food (so Alex has 3 food total), then Alex goes to get water while I stay here and collect the last food. Then we both head to East Shelter. Actually, wait - let me reconsider. We need 2 food + 2 water EACH. I have 2 food, 0 water. Alex has 2 food. If I collect 1 more food (T+98), I'll have 3 food. Then I need 2 water. Fastest water route from Food Grove: East Shelter (15 min) + Central Camp (18 min) + North Ridge (10 min) + Water Source (8 min) = 51 min to get there. That's T+149. Then 5 min to collect = T+154. Return 51 min = T+205. TOO LATE. Alternative: Send Alex to get water while I stay and collect food. Alex leaves now, goes to Water Source (51 min), collects (5 min), returns (51 min) = 107 min total, arrives T+200. Still too late! We're in trouble. We need water NOW. Let me collect this last food quickly, then BOTH head to East Shelter and figure out water there. Actually, the map shows North Ridge connects to Water Source (8 min). From Food Grove: East Shelter (15) + Central Camp (18) + North Ridge (10) = 43 min to North Ridge, then 8 min to Water Source = 51 min total. If we leave NOW (T+93), we arrive Water Source at T+144, collect by T+149, leave by T+149, arrive North Ridge T+157, Central Camp T+167, East Shelter T+185. We arrive at T+185, storm at T+180. We miss it! We need to leave MUCH earlier. We should go NOW without collecting more. We have 2 food each. We just need 2 water each. Let's go to Water Source immediately.

## M20  ·  seq 75  ·  T+108  ·  Sam → Alex
MESSAGE: "Alex, heading to Central Camp then Water Source to get water. Meet me at East Shelter by T+175!"
TRUE STATE: Sam at east_shelter with food 2, water 0; Alex at travelling with food 2, water 2
KNOWS: Water Source has water (unlimited). | Food Grove had 3 food left (you were last there at T+93). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+126 MOVE east_shelter, T+144 WAIT 30, T+174 WAIT 10
NOTE (verbatim): CRITICAL SITUATION at T+108. I'm at East Shelter with 2 food, 0 water. Alex location unknown - last message at T+93 said they were collecting 2 food at Food Grove. I need 2 water ASAP. Time remaining: 72 min until storm/rescue at T+180. WATER PLAN: East Shelter -> Central Camp (18 min, T+126) -> North Ridge (10 min, T+136) -> Water Source (8 min, T+144) -> collect water (5 min, T+149) -> return to East Shelter: Water Source->North Ridge (8 min, T+157) -> Central Camp (10 min, T+167) -> East Shelter (18 min, T+185). ARRIVES T+185 - ONLY 5 MIN LATE but storm hits T+180! This won't work. ALTERNATIVE: Alex must get water while I go to Food Grove. But Alex's location is unknown. I should head to Central Camp (hub) to potentially intercept Alex or get closer to Water Source. Actually, I should go directly toward Water Source NOW. Best path: Central Camp is hub. Let me go there.
