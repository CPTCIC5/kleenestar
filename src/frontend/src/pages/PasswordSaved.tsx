import { FunctionComponent } from "react";
import { Link } from "react-router-dom";
import PrimaryButton from "../components/PrimaryButton";

const PasswordSaved: FunctionComponent = () => {
    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4 flex-col gap-[30px]">
            <div className=" items-center justify-center gap-[18.13px] flex">
                <img className="w-[52.07px] h-[54.78px]" src="/group-672.svg" alt="" />
                <span className="w-[156.02px] font-syne font-[700] text-[25px] leading-[30px]">
                    Kleenestar
                </span>
            </div>
            <div className="max-w-[722px] max-h-[617.62px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 bg-white">
                <div className="max-width flex items-center justify-center box-border max-w-full">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className="font-syne m-0  font-[700] text-[30px] font-inherit inline-block z-[1] leading-[36px] text-primary-300">
                            Password Saved
                        </span>
                        <span className="max-w-[454px] w-full self-stretch text-[16px] leading-[19.5px] text-center font-montserrat z-[1] font-[400] text-primary-300">
                            Your password has been successfuly updated. 🥳
                        </span>
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
                    <Link to={"/"}>
                        <PrimaryButton>Go to login</PrimaryButton>
                    </Link>
                    {/* Use the PrimaryButton component */}
                </div>
            </div>
        </div>
    );
};

export default PasswordSaved;
