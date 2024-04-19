import React, { useState } from "react";

interface ChatButtonProps {
    // define your props here
}

const ChatButton: React.FC<ChatButtonProps> = () => {
    // define your state and methods here

    const [isEditing, setIsEditing] = useState<boolean>(false);
    const [buttonText, setButtonText] = useState<string>("Rename");
    const [newName, setNewName] = useState<string>("");

    const handleClick = () => {
        if (isEditing) {
            if (newName.trim() !== "") {
                setButtonText(newName);
            }
            setIsEditing(false);
        } else {
            setIsEditing(true);
            setNewName(buttonText);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNewName(e.target.value);
    };

    const handleBlur = () => {
        handleClick();
    };

    return (
        <div className="overflow-hidden h-[56px]">
            {isEditing ? (
                <input
                    type="text"
                    className="outline-none border-none mx-[10px] font-syne font-bold text-[15px] text-center text-primary-300 bg-white w-full h-full"
                    value={newName}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    autoFocus
                />
            ) : (
                <button
                    className="outline-none border-none mx-[10px] font-syne font-bold text-[15px] text-primary-300 bg-white w-full overflow-hidden whitespace-nowrap overflow-ellipsis h-full"
                    onClick={handleClick}
                >
                    {buttonText}
                </button>
            )}
        </div>
    );
};

export default ChatButton;
