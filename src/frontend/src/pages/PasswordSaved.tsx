import { FunctionComponent } from "react";
import { Link } from "react-router-dom";

const PasswordSaved: FunctionComponent = () => {
    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4">
            <div className="max-w-[722px] max-h-[617.62px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4">
                <div className="max-width flex items-center justify-center box-border max-w-full text-11xl font-syne">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className=" m-0 text-inherit font-bold font-inherit inline-block z-[1]">
                            Password Saved
                        </span>
                        <div className="max-width self-stretch text-base text-center font-montserrat z-[1] flex flex-col items-center">
                            <span>Your password has been successfuly updated. 🥳 </span>
                        </div>
                    </div>
                </div>

                <div className="max-w-[331.92px] w-full mt-[43.58px]">
                    <img
                        src="/password-saved.jpeg"
                        alt=""
                        className="max-w-full h-auto block m-auto "
                    />
                </div>

                <div className="h-[40px] max-w-[454px] w-full mt-[43.58px]">
                    <Link to={"/"}>Go to login</Link>
                    {/* Use the PrimaryButton component */}
                </div>
            </div>
        </div>
    );
};

export default PasswordSaved;
