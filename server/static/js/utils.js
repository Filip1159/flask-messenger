const renderChats = (chats, active) => {
    const renderedChats = chats.map((c, i) => {
        let modifier = "";
        switch (i) {
            case active - 1:
                modifier = " chatItem--beforeActive";
                break;
            case active:
                modifier = " chatItem--active";
                break;
            case active + 1:
                modifier = " chatItem--afterActive";
                break;
            default:
        }
    })
    return null
}
