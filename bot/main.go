package bot

import (
	"fmt"
	s "github.com/slack-go/slack"
	"log"
	"os"
	"strings"
)

type Client struct {
	Client *s.Client
	Users  []s.User
	Name   string
	Tag    string
	ID     string
}

type Command struct {
	Command  string
	Callback func(channel string, command string)
}

// Global instance
var Bot = &Client{
	Name: "botty_mcbotface",
	Client: s.New(
		os.Getenv("BOT_USER_OAUTH_ACCESS_TOKEN"),
		s.OptionDebug(true),
		s.OptionLog(log.New(os.Stdout, "slack-bot: ", log.Lshortfile|log.LstdFlags)),
	),
}

// GetUserIDByName - Retrieve a users id by their name.
func (bot *Client) GetUserIDByName(name string) string {
	for _, user := range bot.Users {
		if user.Name == name {
			return user.ID
		}
	}

	return ""
}

// isBotMessage - Checks if a message is directed at the bot.
func (bot *Client) isBotMessage(message string) bool {
	return strings.HasPrefix(message, bot.Tag)
}

// handleMessageEvent - Handle messages based on their content.
func (bot *Client) handleMessageEvent(ev *s.MessageEvent) error {
	msgText := ev.Text
	if bot.isBotMessage(msgText) {

		// Get the command send to the bot
		parse := strings.Split(msgText, bot.Tag)
		cmd := strings.TrimSpace(parse[1])

		// Register commands
		switch cmd {
		case Arise.Command:
			Arise.Callback(ev.Channel, cmd)
			break
		}

		log.Println("cmd::", cmd)
		return nil
	}

	return nil
}

// Init - Initialize bot data.
func (bot *Client) Init() {
	users, err := bot.Client.GetUsers()
	if err != nil {
		panic(err)
	}

	bot.Users = users
	bot.ID = bot.GetUserIDByName(bot.Name)
	bot.Tag = fmt.Sprintf("<@%s>", bot.ID)
}

// Run - Starts the RTM listener.
func (bot *Client) Run() {
	log.Println("Initializing bot")
	bot.Init()

	// Start listening slack events
	log.Println("Starting bot rtm listener")
	rtm := bot.Client.NewRTM()
	go rtm.ManageConnection()

	// Handle slack events
	for msg := range rtm.IncomingEvents {
		switch ev := msg.Data.(type) {
		case *s.MessageEvent:
			if err := bot.handleMessageEvent(ev); err != nil {
				log.Printf("[ERROR] Failed to handle message: %s", err)
			}
		}
	}
}
