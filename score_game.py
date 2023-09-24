from pprint import pprint

def get_number_of_players():
    while True:
        try:
            num_players = int(input("Enter the number of players (up to 6): "))
            if 1 <= num_players <= 6:
                return num_players
            else:
                print("The number of players must be between 1 and 6.")
        except ValueError:
            print("Please enter a valid integer.")


def get_player_name(player_number):
    player_name = input(f"Enter the name of Player {player_number}: ")
    return player_name.strip()


def get_player_grid(player_name):
    print(f"Enter the grid for {player_name}.")
    grid = []
    for i in range(4):
        while True:
            row = input(f"Enter row {i + 1} (5 characters): ")
            if len(row) == 5:
                grid.append(list(row.upper()))
                break
            else:
                print("Row must contain exactly 5 characters.")
    return grid


def confirm_player_grid(player_name, player_grid):
    print(f"Here's the grid you've entered for {player_name}:")
    for row in player_grid:
        print("".join(row))
    while True:
        confirmation = input("Is this correct? (y/n): ").strip().lower()
        if confirmation == 'y':
            return True
        elif confirmation == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def initialise_card_info():
    card_info = {
        'C': {'name': 'Coral', 'type': 'Producer'},
        'G': {'name': 'Grouper', 'type': 'Prey'},
        'E': {'name': 'Eel', 'type': 'Predator'},
        'T': {'name': 'Turtle', 'type': 'none'},
        'K': {'name': 'Krill', 'type': 'Producer'},
        'N': {'name': 'Clownfish', 'type': 'Prey'},
        'S': {'name': 'Shark', 'type': 'Predator'},
        'O': {'name': 'Octopus', 'type': 'none'},
        'P': {'name': 'Plankton', 'type': 'Producer'},
        'B': {'name': 'Crab', 'type': 'Prey'},
        'W': {'name': 'Whale', 'type': 'Predator'},
        'F': {'name': 'Flipped', 'type': 'none'}
    }
    return card_info

def update_plankton_scores(player_scores):
    plankton_counts = {player: info['card_scores']['P'] for player, info in player_scores.items()}
    sorted_plankton = sorted(plankton_counts.items(), key=lambda x: x[1], reverse=True)
    points = [12, 8, 4]
    last_score = -1
    last_point = -1

    for i, (player, count) in enumerate(sorted_plankton):
        if count == last_score:
            player_scores[player]['card_scores']['P'] = last_point
        else:
            player_scores[player]['card_scores']['P'] = points[i]
            last_point = points[i]
        last_score = count
    
    # Updating the 'Producer' scores
    for player, info in player_scores.items():
        plankton_score = info['card_scores'].get('P', 0)
        if 'Producer' in info['card_scores']:
            player_scores[player]['card_scores']['Producer'] += plankton_score
        else:
            player_scores[player]['card_scores']['Producer'] = plankton_score

    return player_scores




def score_ecosystem(player_name, grid, card_info):
    player_scores = {}
    producer_count = {}
    prey_count = {}
    predator_count = {}

    # Initialize scores for each card
    for card in card_info:
        player_scores[card] = 0

    # Initialize counts for each ecological type
    for eco_type in ['Producer', 'Prey', 'Predator']:
        producer_count[eco_type] = 0
        prey_count[eco_type] = 0
        predator_count[eco_type] = 0

    # Loop through grid to calculate scores
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            card = grid[i][j]

    # Scoring rules for each card type
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            card = grid[i][j]

            if card == 'C':
                if i == 3:  # Bottom row
                    player_scores['C'] += 3

            elif card == 'G':
                # Count adjacent Krill
                adjacent_krill = 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if 0 <= i + dx < 4 and 0 <= j + dy < 5:
                        if grid[i + dx][j + dy] == 'K':
                            adjacent_krill += 1
                player_scores['G'] += 3 * adjacent_krill

            elif card == 'E':
                adjacent_prey = 0
                adjacent_coral = False
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if 0 <= i + dx < 4 and 0 <= j + dy < 5:
                        if grid[i + dx][j + dy] in ['G', 'N', 'B']:
                            adjacent_prey += 1
                        if grid[i + dx][j + dy] == 'C':
                            adjacent_coral = True
                if adjacent_coral:
                    player_scores['E'] += 4 * adjacent_prey

            #elif card == 'T':
                # Logic handled outside this loop

            #elif card == 'K':
                # Logic handled outside this loop

            elif card == 'N':
                adjacent_score = 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if 0 <= i + dx < 4 and 0 <= j + dy < 5:
                        if grid[i + dx][j + dy] in ['P', 'C']:
                            adjacent_score += 2
                player_scores['N'] += adjacent_score

            #elif card == 'S':
                # Logic handled outside this loop

            elif card == 'O':
                player_scores['O'] += 3

            #elif card == 'P':
                # Logic handled outside this loop

            elif card == 'B':
                # Count the number of Planktons ('P') in the same row
                plankton_count_in_row = sum(1 for col_index in range(5) if grid[i][col_index] == 'P')

                # Calculate the score for this row
                row_score_for_crab = 2 * plankton_count_in_row

                # Add the row score to the player's total score for 'B'
                player_scores['B'] += row_score_for_crab
              
            #elif card == 'W':
                # Logic handled outside this loop

            elif card == 'F':
                pass  # Flipped card, no points
    # Continued logic inside score_ecosystem function

    # Count Turtles in each row and column for 'T' card
    rows_with_turtle = set()
    cols_with_turtle = set()
    for i in range(4):
        for j in range(5):
            if grid[i][j] == 'T':
                rows_with_turtle.add(i)
                cols_with_turtle.add(j)
    player_scores['T'] = 2 * (len(rows_with_turtle) + len(cols_with_turtle))

    # Count connected groups of Krill for 'K' card
    visited = set()
    for i in range(4):
        for j in range(5):
            if grid[i][j] == 'K' and (i, j) not in visited:
                stack = [(i, j)]
                group_size = 0
                while stack:
                    x, y = stack.pop()
                    if (x, y) in visited:
                        continue
                    visited.add((x, y))
                    group_size += 1
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        if 0 <= x + dx < 4 and 0 <= y + dy < 5 and grid[x + dx][y + dy] == 'K':
                            stack.append((x + dx, y + dy))
                player_scores['K'] += 9 if group_size >= 3 else 4 if group_size == 2 else 1

    # Count prey in the same row or column for 'S' card
    for row in range(4):
      for col in range(5):
        if grid[row][col] == 'S':
            row_prey_count = sum(1 for card in grid[row] if card in ['G', 'N', 'B'])
            col_prey_count = sum(1 for row_index in range(4) if grid[row_index][col] in ['G', 'N', 'B'])
            
            player_scores['S'] += 2 * (row_prey_count + col_prey_count)
          
    # Count Plankton for 'P' card (for end game bonus)
    plankton_count = sum(1 for i in range(4) for j in range(5) if grid[i][j] == 'P')
    player_scores['P'] = plankton_count  # This will be used later for end game bonuses

    # Count Krill in ecosystem for 'W' card
    krill_count = sum(1 for i in range(4) for j in range(5) if grid[i][j] == 'K')
    whale_count = sum(1 for i in range(4) for j in range(5) if grid[i][j] == 'W')
    # Update 'W' score for each player
    player_scores['W'] = 2 * krill_count * whale_count

    # Calculate Food Web score
    player_scores['Producer'] = player_scores['C'] + player_scores['K'] # add in P scores after
    player_scores['Prey'] = player_scores['G'] + player_scores['N'] + player_scores['B']
    player_scores['Predator'] = player_scores['E'] + player_scores['S'] + player_scores['W']

    # Return the complete scoring data
    return {
        'player_name': player_name,
        'card_scores': player_scores}


def calculate_food_web(player_scores):
    for player, info in player_scores.items():
        producer_score = info['card_scores'].get('Producer', 0)
        prey_score = info['card_scores'].get('Prey', 0)
        predator_score = info['card_scores'].get('Predator', 0)
        
        # Calculate Food Web score as the minimum among Producer, Prey, and Predator
        food_web_score = min(producer_score, prey_score, predator_score)
        
        # Update the Food Web score in the player_scores dictionary
        info['card_scores']['Food Web'] = food_web_score


def calculate_total(player_scores):
    for player, data in player_scores.items():
        card_scores = data['card_scores']
        
        # Calculate totals for Producer, Prey, Predator, Turtle, Octopus, and Food Web
        total_score = (
            card_scores.get('Producer', 0) + 
            card_scores.get('Prey', 0) + 
            card_scores.get('Predator', 0) + 
            card_scores.get('T', 0) + 
            card_scores.get('O', 0) + 
            card_scores.get('Food Web', 0)
        )
        
        # Add total score to each player's data
        data['total_score'] = total_score

def generate_markdown_table(player_scores, card_info):
    players = [player for player in player_scores]
    player_count = len(players)
    
    # Create the header with proper alignment
    header = "| {:<10} |".format(" ") + " | ".join([f"{player:^10}" for player in players]) + " |"
    
    # Create the divider with the correct number of dashes
    divider = "|{:<11}|".format("-" * 10) + ("{:<11}|".format("-" * 10) * player_count)
    
    markdown_lines = [header, divider]
    
    order = ['C', 'K', 'P', '---', 'G', 'N', 'B', '---', 'E', 'S', 'W', '---', 'Producer', 'Prey', 'Predator', 'Food Web', 'T', 'O', '---']

    for card in order:
        if card == '---':
            row = divider
        else:
            row_name = card_info.get(card, {}).get('name', card)
            row = f"| {row_name:<10} | " + " | ".join([f"{player_scores[player]['card_scores'].get(card, 0):^10}" for player in players]) + " |"
        
        markdown_lines.append(row)
        
    # Generate the 'Total' row
    total_row = f"| {'Total':<10} | " + " | ".join([f"{player_info['total_score']:^10}" for player_info in player_scores.values()]) + " |"
    markdown_lines.append(total_row)

    return "\n" + "\n".join(markdown_lines)  

def main():
    card_info = initialise_card_info()
    num_players = get_number_of_players()
    players = set()
    player_scores = {}

    for i in range(num_players):
        while True:
            player_name = get_player_name(i + 1)

            if player_name not in players:
                players.add(player_name)
                break
            else:
                print("This name has already been used. Please choose a different name.")

        player_grid = get_player_grid(player_name)
        confirmed = confirm_player_grid(player_name, player_grid)

        while not confirmed:
            print("Grid was not confirmed. Please re-enter.")
            player_grid = get_player_grid(player_name)
            confirmed = confirm_player_grid(player_name, player_grid)

        # Calculate and store the player's score
        player_scores[player_name] = score_ecosystem(player_name, player_grid, card_info)
      
    update_plankton_scores(player_scores)
    calculate_food_web(player_scores)
    calculate_total(player_scores)
  
    # Generate the Markdown-formatted output
    markdown_output = generate_markdown_table(player_scores, card_info)
    #print(list(players))
    #print(player_scores)
    with open('output.txt', 'w') as file:
      pprint(player_scores, stream=file)
      
    # Print or save the Markdown output
    print(markdown_output)

if __name__ == "__main__":
    main()
# python score_game.py < input.txt