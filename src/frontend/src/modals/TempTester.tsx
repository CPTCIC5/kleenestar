import React from "react";
// import DeleteChat from "./DeleteChat";
// import ChatFeedback from "./ChatFeedback";
// import GoogleAds from "./GoogleAds";
// import MetaAds from "./MetaAds";
// import TwitterAds from "./TwitterAds";
// import LinkedinAds from "./LinkedinAds";
// import TiktokAds from "./TiktokAds";
// import ArchiveChats from "./ArchiveChats";
import InviteTeam from "./InviteTeam";

interface TempTesterProps {
    // define your props here
}

const TempTester: React.FC<TempTesterProps> = () => {
    const [isOpen, setIsOpen] = React.useState<boolean>(false);
    // const [connected, setConnected] = React.useState<boolean>(false);

    const onClose = (option: boolean) => {
        setIsOpen(!option);
    };

    if (isOpen) {
        document.body.classList.add("overflow-y-hidden");
    } else {
        document.body.classList.remove("overflow-y-hidden");
    }

    return (
        <div className="flex items-center justify-center ">
            <button onClick={() => onClose(isOpen)}>Open Modal</button>
            {isOpen && <InviteTeam isOpen={isOpen} onClose={onClose} />}
        </div>
    );
};

export default TempTester;
