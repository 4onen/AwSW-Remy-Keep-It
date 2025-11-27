init:
    image remyrom remykeepitc = renpy.display.im.Composite((2500,1406),(0,0),"cg/chap4/remyrom.png", (0,0), "remykeepit_4onen/remyrom_lipstick.png")

init python:
    remykeepit_4onen_enabled = False

label remykeepit_4onen_enabled:
    c "Keep it. Its history is pretty outdated for us anyway. Nobody else here would know any of that."

    Ry normal c "I suppose that's true."

    if remystatus == "neutral":
        c "I'd also say it makes you look a little more festive, too. Could be fun at the festival."

        Ry smile c "Well, if you say so."
    else:
        c "I'd also say it accentuates your features well, regardless of your gender."

        Ry shy c "Oh, would you?"

    Ry normal c "Well, it's kind of uncomfortable. I suppose it's not really suited for our scales."

    Ry "But I could keep it on for the rest of today."

    python:
        remykeepit_4onen_enabled = True
        mp.remylipstick = "yes"
        mp.save()

    jump remykeepit_4onen_enabled_end

label remykeepit_4onen_c4_kiss:
    show remyrom remykeepitc at Pan((580, 326), (350, 0), 8.0) with fade
    jump remykeepit_4onen_c4_kiss_end

label remykeepit_4onen_c5_ready:
    c "Lipstick again?"
    Ry shy c "Well, I thought that you liked it last time."
    c "I did say it was festive, yeah."
    Ry normal c "What better time to wear it than the finale of the festival?"
    c "Makes sense to me. Let's go see those fireworks then, huh?"
    jump remykeepit_4onen_c5_ready_return