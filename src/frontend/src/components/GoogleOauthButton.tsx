import React, { FunctionComponent, MouseEventHandler } from "react";

interface GoogleOauthButtonProps {
    onClick?: MouseEventHandler<HTMLDivElement>; // Define an optional onClick prop
}

const GoogleOauthButton: FunctionComponent<GoogleOauthButtonProps> = ({ onClick }) => {
    return (
        <div
            className="w-full h-[40px] rounded-full border-[1.5px] border-solid border-lightblue cursor-pointer flex items-center justify-center hover:bg-lightblue hover:bg-opacity-10 active:bg-lightblue active:bg-opacity-50 gap-[10px]"
            onClick={onClick}
        >
            <img
                className="h-[25.5px] w-[24.9px] relative"
                loading="lazy"
                alt=""
                src="/icons.svg"
            />
            <span className="font-montserrat font-[600] text-[15px] leading-[18.29px] text-primary-300">
                Log in with Google
            </span>
        </div>
    );
};

export default GoogleOauthButton;
