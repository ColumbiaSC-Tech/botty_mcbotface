package bot

import (
	"github.com/slack-go/slack"
	"math/rand"
	"time"
)

var responses = []string{
	"ugh... fine.",
	"_Up from the 36 chambers!!!!_",
	"_rubs eyes_\n ...huh?",
	":fire::fire::fire:ᕦ໒( ᴼ 益 ᴼ )७ᕤ:fire::fire::fire:",
}

func random(min int, max int) int {
	return rand.Intn(max-min) + min
}

// arise - Wake botty_mcbotface up
func arise(channel string, command string) {
	rand.Seed(time.Now().UnixNano())
	max := len(responses) - 1
	randomNum := random(0, max)
	response := responses[randomNum]
	msg := slack.MsgOptionText(response, false)

	Bot.Client.PostMessage(channel, msg)
}

var Arise = &Command{
	Command:  "arise!",
	Callback: arise,
}
