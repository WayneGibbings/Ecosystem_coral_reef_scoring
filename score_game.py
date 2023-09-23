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


def confirm_player_grid(player_grid):
    print(f"Here's the grid you've entered for {player_name}:")
    for row in grid:
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
            card_type = card_info[card]['type']

            # Scoring rules for each card type
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
                adjacent_score = 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if 0 <= i + dx < 4 and 0 <= j + dy < 5:
                        if grid[i + dx][j + dy] == 'P':
                            adjacent_score += 2
                player_scores['B'] += adjacent_score

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

    # Count Prey in same row or column for 'S' card
    for i in range(4):
        for j in range(5):
            if grid[i][j] == 'S':
                row_prey_count = sum(1 for card in grid[i] if card in ['G', 'N', 'B'])
                col_prey_count = sum(1 for x in range(4) if grid[x][j] in ['G', 'N', 'B'])
                player_scores['S'] += 2 * (row_prey_count + col_prey_count)

    # Count Plankton for 'P' card (for end game bonus)
    plankton_count = sum(1 for i in range(4) for j in range(5) if grid[i][j] == 'P')
    player_scores['P'] = plankton_count  # This will be used later for end game bonuses

    # Count Krill in ecosystem for 'W' card
    krill_count = sum(1 for i in range(4) for j in range(5) if grid[i][j] == 'K')
    player_scores['W'] = 2 * krill_count

    # Calculate Food Web score
    player_scores['Producer'] = player_scores['Coral'] + player_scores['Krill']
    player_scores['Prey'] = player_scores['Grouper'] + player_scores['Clownfish']
    player_scores['Predator'] = player_scores['Eel'] + player_scores['Shark']
    
    # Calculate Food Web score
    player_scores['Food Web'] = calculate_food_web(player_scores)

    # Return the complete scoring data
    return {
        'player_name': player_name,
        'card_scores': player_scores,
        'producer_count': sum(producer_count.values()),
        'prey_count': sum(prey_count.values()),
        'predator_count': sum(predator_count.values())}


def calculate_food_web(player_scores):
    producer_score = player_scores.get('Producer', 0)
    prey_score = player_scores.get('Prey', 0)
    predator_score = player_scores.get('Predator', 0)
    
    # Calculate Food Web score as minimum among Producer, Prey, and Predator
    food_web_score = min(producer_score, prey_score, predator_score)
    
    return food_web_score


def special_scoring_rules(player_data_list):
    pass

def generate_markdown_output(players, scores):
    # Initialize an empty list to store Markdown-formatted lines
    markdown_lines = []
    
    # Add the header row with player names
    header = "| Metric | " + " | ".join([player for player in players]) + " |"
    markdown_lines.append(header)
    
    # Add the separator row
    separator = "| --- | " + " | ".join(["---" for _ in players]) + " |"
    markdown_lines.append(separator)
    
    # Add the rows for each card
    for card in ['Coral', 'Krill', 'Plankton', 'Grouper', 'Clownfish', 'Crab', 'Eel', 'Shark', 'Whale']:
        row = f"| {card} | " + " | ".join([str(scores[player][card]) for player in players]) + " |"
        markdown_lines.append(row)
    
    # Add the rows for additional metrics
    for metric in ['Producer', 'Prey', 'Predator', 'Food Web', 'Turtle', 'Octopus']:
        row = f"| {metric} | " + " | ".join([str(scores[player].get(metric, 0)) for player in players]) + " |"
        markdown_lines.append(row)
    
    # Add the total row
    row = "| Total | " + " | ".join([str(sum(scores[player].values())) for player in players]) + " |"
    markdown_lines.append(row)
    
    # Combine all lines into a single Markdown-formatted string
    markdown_output = "\n".join(markdown_lines)
    
    return markdown_output

def main():
    initialise_card_info()
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
        confirmed = confirm_player_grid(player_grid)
        
        while not confirmed:
            print("Grid was not confirmed. Please re-enter.")
            player_grid = get_player_grid(player_name)
            confirmed = confirm_player_grid(player_grid)

        # Calculate and store the player's score
        player_scores[player_name] = score_ecosystem(player_grid)
        
    # Generate the Markdown-formatted output
    markdown_output = generate_markdown_output(list(players), player_scores)
    
    # Print or save the Markdown output
    print(markdown_output)

if __name__ == "__main__":
    main()

