import React from "react";
import DeleteChat from "./DeleteChat";
import ChatFeedback from "./ChatFeedback";

interface TempTesterProps {
    // define your props here
}

const TempTester: React.FC<TempTesterProps> = () => {
    const [isOpen, setIsOpen] = React.useState<boolean>(false);

    const onClose = () => {
        setIsOpen(!isOpen);
    };

    if (isOpen) {
        document.body.classList.add("overflow-y-hidden");
    } else {
        document.body.classList.remove("overflow-y-hidden");
    }

    return (
        <div className="flex items-center justify-center ">
            <button onClick={onClose}>Open Modal</button>
            {isOpen && <ChatFeedback isOpen={isOpen} onClose={onClose} />}
        </div>
    );
};

export default TempTester;
