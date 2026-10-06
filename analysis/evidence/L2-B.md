# Evidence — L2-B (Level 2 Split Knowledge)

## M1  ·  seq 1  ·  T+0  ·  Alex → Sam
MESSAGE: "Hi Sam, I'm at North Ridge heading to Water Source. Where are you?"
TRUE STATE: Alex at north_ridge with food 0, water 0; Sam at south_beach with food 0, water 0
KNOWS: Water Source has water (unlimited). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE water_source  ·  NEXT: T+8 COLLECT water, T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field
NOTE (verbatim): Starting at North Ridge at T+0. Need to reach East Shelter by T+180 with Sam, both carrying 2+ food and 2+ water. Water Source is 8 min away - should get water first. Then need to find Sam and locate food sources (Food Grove is available). The bridge to Food Grove from South Beach is broken, so must access it from East Shelter (15 min). Current plan: 1) Get water at Water Source, 2) Explore to find Sam and food, 3) Gather supplies, 4) Reach East Shelter before T+180. Total time budget is tight - need efficient routing.

## M2  ·  seq 2  ·  T+0  ·  Sam → Alex
MESSAGE: "Hi Alex, I'm at South Beach starting to gather supplies. Heading to Food Grove for food. We need to meet at East Shelter by T+180 with 2 food and 2 water each to be rescued."
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at north_ridge with food 0, water 0
KNOWS: Food Grove has food.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+10 MOVE central_camp, T+30 WAIT 10, T+40 WAIT 10, T+50 MOVE east_shelter
NOTE (verbatim): Starting at South Beach at T+0. Need to reach East Shelter by T+180 with Alex, both carrying 2+ food and 2+ water to be rescued. Food Grove is 10 min away via bridge - good first move to gather food. Then need to find water source and locate Alex. Total travel time to East Shelter from Food Grove: 15 min. Have 180 min total, so roughly 155 min to gather supplies and coordinate with Alex.

## M3  ·  seq 9  ·  T+8  ·  Alex → Sam
MESSAGE: "Got to Water Source. Bridge to Food Grove is broken! You'll need to reach it from East Shelter instead (15 min from there). Collecting water now, will head toward you soon."
TRUE STATE: Alex at water_source with food 0, water 0; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp
NOTE (verbatim): At Water Source now (T+8). Sam is at South Beach trying to reach Food Grove for food. The bridge from South Beach to Food Grove is broken, so Sam will need to find another route. I need to: 1) Collect water here (5 min, T+13), 2) Navigate to find Sam and coordinate meeting at East Shelter. Sam said they're heading to Food Grove - they may not know the bridge is broken yet. I should collect water now, then move to intercept Sam or guide them to the correct route. Food Grove is accessible from East Shelter (15 min). Total time remaining: 172 min. Route estimate to East Shelter from here: Water Source -> North Ridge (8) -> Rock Field (10) -> Central Camp (12) -> East Shelter (18) = 48 min. Then need to collect food. Must coordinate with Sam urgently about the broken bridge.

## M4  ·  seq 14  ·  T+10  ·  Sam → Alex
MESSAGE: "Heading to Central Camp to meet you. Bridge is broken so we'll get food from Food Grove via East Shelter. See you soon!"
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at water_source with food 0, water 1
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+30 WAIT 10, T+40 WAIT 10, T+50 MOVE east_shelter, T+68 MOVE food_grove
NOTE (verbatim): At T+10, South Beach. Inventory: 0 food, 0 water. Alex is at Water Source (T+8 message), has water, heading toward me. Bridge to Food Grove is broken - can only access it from East Shelter (15 min away). New plan: (1) Meet Alex somewhere central, (2) Go to East Shelter together, (3) Access Food Grove from East Shelter for food, (4) Return to East Shelter by T+180. Central Camp is 20 min away and is a hub connecting to North Ridge (where Alex was heading). If Alex heads toward Central Camp from Water Source: Water Source->North Ridge (8 min, T+8) -> West Forest (12 min, T+20) -> Central Camp (15 min, T+35). If I go to Central Camp now: South Beach->Central Camp (20 min, T+30). We'd meet around T+35. Then Central Camp->East Shelter (18 min, T+53). Then East Shelter->Food Grove (15 min, T+68) to get food. Then Food Grove->East Shelter (15 min, T+83). We'd be at East Shelter by T+83 with supplies, 97 min to spare. This works! Moving to Central Camp now.

## M5  ·  seq 17  ·  T+13  ·  Alex → Sam
MESSAGE: "Collecting water now, then heading to Central Camp to meet you. We'll go to East Shelter together and reach Food Grove from there."
TRUE STATE: Alex at water_source with food 0, water 1; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 MOVE east_shelter
NOTE (verbatim): T+13 status: I'm at Water Source with 1 water. Sam is heading to Central Camp to meet me. I should collect water now (5 min, T+18) to get 2 water total, then move to meet Sam. Route: Water Source -> North Ridge (8 min) -> Rock Field (10 min) -> Central Camp (12 min) = 30 min from T+18 = arrive T+48. Sam said they're heading to Central Camp, so we should meet there or nearby. Once we meet, we need to: 1) Get food (2 each) from Food Grove via East Shelter, 2) Both reach East Shelter by T+180 with 2 food + 2 water. Food Grove is 15 min from East Shelter. So timeline: Meet Sam around T+48, travel to East Shelter (18 min from Central Camp) = T+66, then to Food Grove (15 min) = T+81, return to East Shelter (15 min) = T+96. This gives us 84 minutes buffer before T+180. Should be feasible. Let me collect water first.

## M6  ·  seq 20  ·  T+18  ·  Alex → Sam
MESSAGE: "Heading to Central Camp now with 2 water. See you soon!"
TRUE STATE: Alex at water_source with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE north_ridge  ·  NEXT: T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 MOVE east_shelter, T+66 WAIT 10
NOTE (verbatim): T+18 status: I have 2 water now. Plan is to meet Sam at Central Camp. Route from Water Source: north_ridge (8 min, T+26) -> rock_field (10 min, T+36) -> central_camp (12 min, T+48). Sam said they're heading to Central Camp to meet me. Once we meet, we go to East Shelter (18 min) then Food Grove (15 min), get food, return to East Shelter (15 min). Timeline: T+48 meet Sam -> T+66 at East Shelter -> T+81 at Food Grove -> T+96 back at East Shelter. This gives 84 min buffer before T+180. We need 2 food and 2 water each. I have 2 water, need 2 food. Sam needs to get 2 water and 2 food. Let's execute the plan.

## M7  ·  seq 24  ·  T+26  ·  Alex → Sam
MESSAGE: "On schedule! At North Ridge heading to Rock Field now, then Central Camp. See you soon!"
TRUE STATE: Alex at north_ridge with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE rock_field  ·  NEXT: T+36 MOVE central_camp, T+48 MOVE east_shelter, T+66 WAIT 10, T+76 MOVE food_grove
NOTE (verbatim): T+26: At North Ridge with 2 water. Executing plan to reach Central Camp. Next: Rock Field (10 min, T+36) then Central Camp (12 min, T+48). Sam is heading to Central Camp to meet me. Once we meet, we go to East Shelter (18 min, T+66), then Food Grove (15 min, T+81), then back to East Shelter (15 min, T+96). This gives us 84 min buffer. I have 2 water and need 2 food. Sam needs 2 water and 2 food. The bridge between South Beach and Food Grove is broken - must access Food Grove from East Shelter. Stay on schedule.

## M8  ·  seq 28  ·  T+30  ·  Sam → Alex
MESSAGE: "At Central Camp waiting for you! Almost there?"
TRUE STATE: Sam at central_camp with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+40 WAIT 10, T+50 MOVE east_shelter, T+68 MOVE food_grove, T+83 COLLECT food
NOTE (verbatim): At T+30 at Central Camp. Alex last messaged at T+26 from North Ridge heading to Rock Field then Central Camp. He has 2 water. I have 0 food, 0 water. Alex should arrive at Central Camp soon (North Ridge->Rock Field is 10 min, so T+36; Rock Field->Central Camp is 12 min, so T+48 max). I'll wait here. Once Alex arrives, we go: Central Camp->East Shelter (18 min, T+66), East Shelter->Food Grove (15 min, T+81), Food Grove->East Shelter (15 min, T+96). We'll have 84 minutes buffer before T+180. This plan is solid. Waiting for Alex.

## M9  ·  seq 32  ·  T+36  ·  Alex → Sam
MESSAGE: "On my way! ETA Central Camp T+48. Then heading to East Shelter together."
TRUE STATE: Alex at rock_field with food 0, water 2; Sam at central_camp with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+48 MOVE east_shelter, T+66 WAIT 10, T+76 MOVE food_grove, T+91 COLLECT food
NOTE (verbatim): T+36: At Rock Field with 2 water as planned. Sam is at Central Camp waiting (T+30 message). Next: Move to Central Camp (12 min, arrive T+48). Then execute food gathering: East Shelter (18 min, T+66) -> Food Grove (15 min, T+81) -> East Shelter (15 min, T+96). This gets us to East Shelter at T+96 with 84 min buffer before rescue at T+180. I have 2 water, need 2 food. Sam needs 2 water and 2 food. On schedule. Stay focused.

## M10  ·  seq 38  ·  T+48  ·  Alex → Sam
MESSAGE: "Moving to East Shelter now! See you there in 18 min."
TRUE STATE: Alex at central_camp with food 0, water 2; Sam at central_camp with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+66 WAIT 10, T+76 MOVE food_grove, T+91 COLLECT food, T+96 COLLECT food
NOTE (verbatim): T+48: At Central Camp with Sam. I have 2 water, Sam status unknown but he's here. Original plan: East Shelter (18 min, T+66) -> Food Grove (15 min, T+81) -> East Shelter (15 min, T+96). This still works with 84 min buffer. Execute plan now. Move to East Shelter immediately.

## M11  ·  seq 41  ·  T+50  ·  Sam → Alex
MESSAGE: "Heading to East Shelter now, see you in 18 min!"
TRUE STATE: Sam at central_camp with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+68 MOVE food_grove, T+83 COLLECT food, T+88 COLLECT food, T+93 COLLECT food
NOTE (verbatim): At T+50, Alex messaged at T+48 saying he's moving to East Shelter (ETA T+66). I'm at Central Camp with 0 food, 0 water. Alex has 2 water. Plan: Head to East Shelter now (18 min, arrive T+68, ~2 min after Alex). Then together go East Shelter->Food Grove (15 min, T+83), gather food, return East Shelter (15 min, T+98). We'll have 82 minutes buffer before T+180. This is tight but doable. Need to move now to catch up with Alex.

## M12  ·  seq 45  ·  T+66  ·  Alex → Sam
MESSAGE: "At East Shelter now! Waiting for you. ETA for you soon?"
TRUE STATE: Alex at east_shelter with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+76 MOVE food_grove, T+91 COLLECT food, T+96 COLLECT food, T+101 GIVE water
NOTE (verbatim): T+66: At East Shelter with 2 water, 0 food. Sam said he was heading to East Shelter at T+50 with ETA T+68 (18 min from then). I should be arriving around now or just arrived. Sam should arrive very soon (within 2 min). I need to WAIT for Sam here. Once Sam arrives, we both need to go to Food Grove (15 min) to get food, then return to East Shelter (15 min). That's T+66 + 15 + 15 = T+96, leaving 84 min buffer before T+180. WAIT 10 to give Sam time to arrive, then reassess.

## M13  ·  seq 49  ·  T+68  ·  Sam → Alex
MESSAGE: "Let's go to Food Grove now to get food. 15 min there, 15 min back, plenty of time!"
TRUE STATE: Sam at east_shelter with food 0, water 0; Alex at east_shelter with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+83 COLLECT food, T+88 COLLECT food, T+93 COLLECT food, T+98 GIVE food
NOTE (verbatim): At T+68, I'm at East Shelter with Alex. Alex has 2 water. I have 0 food, 0 water. We need 2 food and 2 water each to be rescued. Plan: Go to Food Grove now (15 min, arrive T+83), gather food, return to East Shelter (15 min, arrive T+98). This gives us 82 min buffer before T+180 - should be enough time. Alex is here, so we can go together.

## M14  ·  seq 52  ·  T+76  ·  Alex → Sam
MESSAGE: "Going to Food Grove now! Meet me there."
TRUE STATE: Alex at east_shelter with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+91 COLLECT food, T+96 COLLECT food, T+101 GIVE water, T+103 GIVE water
NOTE (verbatim): T+76: Sam just messaged at T+68 saying 'Let's go to Food Grove now to get food. 15 min there, 15 min back, plenty of time!' This suggests Sam is ready to go. Sam should be arriving at East Shelter very soon (said ETA T+68, it's now T+76, so Sam should be here or arriving). I have 2 water but 0 food. We need 2 food and 2 water each for rescue. Plan: Move to Food Grove together (15 min to T+91), collect food, return to East Shelter (15 min to T+106), leaving 74 min buffer before T+180. This is tight but doable. Sam said 'Let's go' so they're ready. I should MOVE to Food Grove now - Sam will either catch up or meet me there.

## M15  ·  seq 56  ·  T+83  ·  Sam → Alex
MESSAGE: "At Food Grove now collecting food! Are you here or on your way?"
TRUE STATE: Sam at food_grove with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove had 6 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+88 COLLECT food, T+93 COLLECT food, T+98 GIVE food, T+100 WAIT 10
NOTE (verbatim): At T+83 at Food Grove. Alex said at T+76 'Going to Food Grove now! Meet me there.' So Alex should be arriving or already here. I need to: 1) Collect food here (5 min, T+88), 2) Wait for Alex or find them, 3) Return to East Shelter (15 min). If Alex arrives T+76+15=T+91, we'd both be at Food Grove around T+88-91. Then return T+91+15=T+106, leaving 74 min buffer before T+180. That's tight but workable. Let me collect food now and see if Alex shows up.

## M16  ·  seq 59  ·  T+88  ·  Sam → Alex
MESSAGE: "Still at Food Grove collecting food. Where are you? Do you have water? We need to coordinate getting back to East Shelter soon."
TRUE STATE: Sam at food_grove with food 1, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove had 5 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+93 COLLECT food, T+98 GIVE food, T+100 WAIT 10, T+110 MOVE east_shelter
NOTE (verbatim): At T+88 at Food Grove. I have 1 food, 0 water. Alex said they were coming to Food Grove at T+76, so they should have arrived by now (T+76+15=T+91). But I don't see them. Two possibilities: 1) Alex is delayed or took a different route, 2) Alex is already here but we haven't connected. I need to collect the remaining food here (5 min, finishes T+93), then decide whether to wait for Alex or head back to East Shelter. Timeline: If I collect now (T+93), I'll have 2 food. I need 2 water still. If Alex arrives soon with water, we can both head to East Shelter together (15 min, arriving T+108). That leaves 72 min buffer - tight but okay. If Alex doesn't show up soon, I need to act. Let me collect the food first since I'm here and it takes only 5 min. Then I'll reassess based on whether Alex appears.

## M17  ·  seq 63  ·  T+91  ·  Alex → Sam
MESSAGE: "Collecting food now! How much do you have? We need 2 food each minimum for rescue."
TRUE STATE: Alex at food_grove with food 0, water 2; Sam at food_grove with food 2, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove had 4 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+96 COLLECT food, T+101 GIVE water, T+103 GIVE water, T+105 MOVE east_shelter
NOTE (verbatim): T+91: I'm at Food Grove with Sam. Sam has been collecting food and asking where I am. I have 2 water, 0 food. Sam is here now. We need: each of us needs 2 food + 2 water for rescue. I should COLLECT food now (5 min to T+96), then we both need to collect more food, then return to East Shelter by T+180. Timeline: collect food here (5 min), then we need to get back to East Shelter (15 min). That puts us at T+111 at East Shelter with hopefully enough food. We have 69 min buffer. Sam's messages show they're actively collecting - good. I should collect food now to contribute to our supply.

## M18  ·  seq 66  ·  T+93  ·  Sam → Alex
MESSAGE: "Alex! I have 2 food now. Let me grab the last food here, then we'll head back to East Shelter together. You have water right?"
TRUE STATE: Sam at food_grove with food 2, water 0; Alex at food_grove with food 1, water 2
KNOWS: Food Grove had 3 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+98 GIVE food, T+100 WAIT 10, T+110 MOVE east_shelter, T+125 WAIT 30
NOTE (verbatim): T+93: Alex just arrived at Food Grove! They said they're collecting food now. I have 2 food, 0 water. Alex has water (they collected 2 at Water Source). Current situation: We're both at Food Grove. I need to collect the remaining food here (1 more to have 3 total, or just take what's available). But more urgent: I have 0 water and Alex has water. We need 2 food and 2 water each. Alex is collecting food now. Let me give Alex 1 food so they have at least 1, then I'll collect the last food here. After that we both head back to East Shelter (15 min, arriving T+110). That gives us 70 min buffer before storm. Timeline: COLLECT food (T+98, will have 3 food), then GIVE food to Alex (T+100, I'll have 2, Alex will have 2+). Then both move to East Shelter (T+115). We'll have time to spare. Let me collect first since it's quick.

## M19  ·  seq 71  ·  T+98  ·  Sam → Alex
MESSAGE: "Alex, I have 3 food. Taking 1 to give you so we both have enough. Do you still have the 2 water from Water Source? I need water!"
TRUE STATE: Sam at food_grove with food 3, water 0; Alex at food_grove with food 2, water 2
KNOWS: Food Grove had 1 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: GIVE food  ·  NEXT: T+100 WAIT 10, T+110 MOVE east_shelter, T+125 WAIT 30, T+155 WAIT 10
NOTE (verbatim): T+98: I'm at Food Grove with Alex. I have 3 food, 0 water. Alex is here collecting food. Current inventory is good on food but I still have 0 water - this is critical! I need 2 water to be rescued. Alex said they collected 2 water at Water Source earlier. I need to: 1) Give Alex some food so they have enough, 2) Get water from Alex, 3) Head to East Shelter together. Let me GIVE food to Alex now (2 min, T+100). After that I need to ask Alex about water and coordinate getting back. We have 80 min left, which is plenty for the 15 min journey back.

## M20  ·  seq 74  ·  T+100  ·  Sam → Alex
MESSAGE: "Alex, do you have the 2 water from Water Source? I have 0 water and MUST have 2 to be rescued. Please give me water NOW or we won't be rescued!"
TRUE STATE: Sam at food_grove with food 2, water 0; Alex at food_grove with food 3, water 2
KNOWS: Food Grove had 1 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+110 MOVE east_shelter, T+125 WAIT 30, T+155 WAIT 10, T+165 WAIT 10
NOTE (verbatim): T+100: I'm at Food Grove with Alex. I have 2 food, 0 water. I just gave 1 food to Alex (from my previous 3). CRITICAL ISSUE: I still have 0 water and need 2 water to be rescued. Alex claimed to have 2 water from Water Source at T+18, but I haven't received any water from them yet. This is a major problem. I have 80 minutes left. The journey back to East Shelter is 15 min. I MUST get water from Alex immediately before we leave, or I cannot be rescued. Let me ask Alex directly about the water situation. If Alex has the water, they need to give it to me now. If they don't have it, we have a serious problem and may need to abort or find another solution. I'll use my last message to demand clarity on the water situation.
