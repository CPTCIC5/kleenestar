import React from "react";

interface PrimaryButtonProps {
    children: React.ReactNode;
    onClick?: () => void; // onClick prop is optional
}

const PrimaryButton: React.FC<PrimaryButtonProps> = ({ children, onClick }) => {
    return (
        <button
            className="cursor-pointer bg-primary-300 text-white rounded-full w-full h-full  shrink-0 border-none p-0 self-stretch  mx-auto font-montserrat font-[600] text-[15px] leading-[18.29px] text-center flex items-center justify-center"
            onClick={onClick} // Use onClick prop
        >
            {children}
        </button>
    );
};

export default PrimaryButton;
