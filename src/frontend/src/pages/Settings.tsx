import { FunctionComponent } from "react";
import FrameComponent18 from "../components/FrameComponent18";
import PasswordUpdate from "../components/PasswordUpdate";
import FrameComponent16 from "../components/FrameComponent16";
import FrameComponent15 from "../components/FrameComponent15";

const Settings: FunctionComponent = () => {
  return (
    <div className="w-full relative bg-whitesmoke flex flex-col items-end justify-start pt-[69px] pb-[97px] pr-[108.30000000000018px] pl-[50px] box-border gap-[40.09999999999991px] tracking-[normal] mq750:gap-[20px_40.1px] mq750:pl-[25px] mq750:pr-[54px] mq750:box-border mq450:pr-5 mq450:box-border">
      <FrameComponent18 />
      <form className="m-0 w-[1294.7px] flex flex-row items-start justify-start pt-0 px-0 pb-[22.700000000000045px] box-border gap-[36.099999999999454px] max-w-full lg:flex-wrap mq750:gap-[36.1px_18px]">
        <PasswordUpdate />
        <FrameComponent16 />
      </form>
      <FrameComponent15 />
    </div>
  );
};

export default Settings;
