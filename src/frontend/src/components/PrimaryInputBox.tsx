import React from "react";

interface PrimaryInputBoxProps {
    type?: string;
    name?: string;
    placeholder?: string;
    className?: string;
    value?: string;
    required?: boolean;
    onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const PrimaryInputBox: React.FC<PrimaryInputBoxProps> = ({
    type = "text",
    name = "",
    placeholder = "",
    className = "",
    value = "",
    required = false,
    onChange,
}) => {
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (onChange) {
            onChange(event);
        }
    };

    return (
        <input
            type={type}
            name={name}
            placeholder={placeholder}
            onChange={handleInputChange}
            value={value}
            className={`bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary  text-opacity-50 outline-none ${className}`}
            required={required}
        />
    );
};

export default PrimaryInputBox;
