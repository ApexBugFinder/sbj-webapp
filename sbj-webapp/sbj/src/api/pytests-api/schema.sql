DROP DATABASE IF EXISTS sbj

USE master
GO
-- Create the new database if it does not exist already
IF NOT EXISTS (
  SELECT name
    FROM sys.databases
    WHERE name = N'sbj'
)
CREATE DATABASE sbj
GO
CREATE DATABASE sbj

DROP TABLE IF EXISTS playershands;
DROP TABLE IF EXISTS handcards;
DROP TABLE IF EXISTS gameresults
DROP TABLE IF EXISTS gameplayers;
DROP TABLE IF EXISTS  gamedecks;
DROP TABLE IF EXISTS  players;
DROP TABLE IF EXISTS hands;
DROP TABLE IF EXISTS  results;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS decks;
DROP TABLE IF EXISTS cards;



CREATE TABLE cards(
    id  SERIAL PRIMARY KEY  NOT NULL,
    h_value INTEGER NULL default 0,
    l_value INTEGER NULL default 0,
    face TEXT NULL UNIQUE,
    suite TEXT NULL,
    url TEXT NULL
    )

CREATE TABLE decks (
  id SERIAL PRIMARY KEY NOT NULL,
  created_at DATETIME NOT NULL DEFAULT now()
)

CREATE TABLE games(
  id SERIAL PRIMARY KEY NOT NULL,
  game_status VARCHAR(10),
  started_at DATETIME NOT NULL DEFAULT now(),
  finished_at DATETIME
)

CREATE TABLE hands(
  id SERIAL PRIMARY KEY NOT NULL,
  status VARCHAR(10) NOT NULL DEFAULT 'ACTIVE',
  player_limit INTEGER NOT NULL DEFAULT 0,
  h_value INTEGER NOT NULL DEFAULT 0,
  l_value INTEGER NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT now()
)

CREATE TABLE players(
  id SERIAL PRIMARY KEY NOT NULL,
  name VARCHAR(128) NOT NULL,
  limit INTEGER NOT NULL DEFAULT 0,
  create_at DATETIME NOT NULL DEFAULT now()
)

CREATE TABLE results(
  id SERIAL PRIMARY KEY NOT NULL,
  pot INTEGER NOT NULL DEFAULT 0,
  player INTEGER NOT NULL DEFAULT 0,
  dealer INTEGER NOT NULL DEFAULT 0
)

CREATE TABLE deckcards(
  deck_id INTEGER NOT NULL,
  card_id INTEGER NOT NULL,
  CONSTRAINT fk_deckcards_deck
    FOREIGN KEY (deck_id)
      REFERENCES decks(id),
  CONSTRAINT fk_deckcards_card
    FOREIGN KEY (card_id)
      REFERENCES cards(id),
  PRIMARY KEY(deck_id, card_id)
)

CREATE TABLE gamedecks(
  game_id INTEGER NOT NULL,
  deck_id INTEGER NOT NULL,
  CONSTRAINT fk_gamedecks_game
    FOREIGN KEY (game_id)
      REFERENCES games(id),
  CONSTRAINT fk_gamedecks_deck
    FOREIGN KEY (deck_id)
      REFERENCES decks(id),
  PRIMARY KEY(game_id, deck_id)
)


CREATE TABLE gameplayers(
  game_id INTEGER NOT NULL,
  player_id INTEGER NOT NULL,
  CONSTRAINT fk_gameplayers_game
    FOREIGN KEY (game_id)
      REFERENCES games(id),
  CONSTRAINT fk_gameplayers_player
    FOREIGN KEY (player_id)
      REFERENCES players(id),
  PRIMARY KEY(game_id, player_id)
)

CREATE TABLE handcards(
  hand_id INTEGER NOT NULL,
  card_id INTEGER NOT NULL,
  CONSTRAINT fk_handcards_hand
    FOREIGN KEY (hand_id)
      REFERENCES hands(id),
  CONSTRAINT fk_handcards_card
    FOREIGN KEY (card_id)
      REFERENCES cards(id),
  PRIMARY KEY(hand_id, card_id)
)


CREATE TABLE playerhands(
  player_id INTEGER NOT NULL,
  hand_id INTEGER NOT NULL,
  CONSTRAINT fk_playerhands_player
    FOREIGN KEY (player_id)
      REFERENCES players(id),
  CONSTRAINT fk_playerhands_hand
    FOREIGN KEY (hand_id)
      REFERENCES hands(id),
  PRIMARY KEY(player_id, hand_id)
)

CREATE TABLE gameresults(
  game_id INTEGER NOT NULL,
  result_id INTEGER NOT NULL,
  CONSTRAINT fk_gameresults_game
    FOREIGN KEY (game_id)
      REFERENCES games(id),
  CONSTRAINT fk_gameresults_result
    FOREIGN KEY (result_id)
      REFERENCES results(id),
  PRIMARY KEY(game_id, result_id)
)