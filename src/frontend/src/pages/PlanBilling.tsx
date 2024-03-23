import { FunctionComponent } from "react";
import ConditionSplitter from "../components/ConditionSplitter";
import FrameComponent27 from "../components/FrameComponent27";

const PlanBilling: FunctionComponent = () => {
  return (
    <div className="w-full relative bg-whitesmoke flex flex-col items-start justify-start pt-[73px] px-[50px] pb-[72.89999999999999px] box-border gap-[55.10000000000002px] tracking-[normal] text-left text-mini text-darkslateblue-100 font-montserrat lg:pl-[25px] lg:pr-[25px] lg:box-border mq750:gap-[28px_55.1px]">
      <ConditionSplitter />
      <div className="w-[1218.7px] flex flex-row items-start justify-center max-w-full">
        <div className="w-[948.7px] flex flex-row items-start justify-between gap-[20px] max-w-full mq750:flex-wrap">
          <div className="w-[162.1px] flex flex-col items-start justify-start">
            <div className="relative inline-block min-w-[57.1px] z-[1]">
              Invoice
            </div>
          </div>
          <div className="w-[119.9px] flex flex-col items-start justify-start">
            <div className="relative inline-block min-w-[66.7px] z-[1]">
              Amount
            </div>
          </div>
          <div className="flex flex-col items-start justify-start py-0 pr-[27.899999999999864px] pl-0">
            <div className="relative inline-block min-w-[39.2px] z-[1]">
              Date
            </div>
          </div>
          <div className="relative inline-block min-w-[50.8px] z-[1]">
            Status
          </div>
          <div className="relative inline-block min-w-[44.4px] z-[1]">
            Users
          </div>
        </div>
      </div>
      <section className="w-[1097.4px] flex flex-row items-start justify-center pt-0 px-0 pb-[9.999999999999917px] box-border max-w-full">
        <FrameComponent27 />
      </section>
      <div className="w-[383.5px] flex flex-row items-start justify-start py-0 pr-16 pl-[63.700000000000045px] box-border max-w-full text-base mq450:pl-5 mq450:pr-5 mq450:box-border">
        <div className="flex-1 relative [text-decoration:underline] shrink-0">
          I need help with a billing issue
        </div>
      </div>
    </div>
  );
};

export default PlanBilling;
