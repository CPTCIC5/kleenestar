import { FunctionComponent } from "react";

export type FrameComponent28Type = {
  chatList?: string;
  rectangle522?: string;
  rectangle5221?: string;
  group1949?: string;
};

const FrameComponent28: FunctionComponent<FrameComponent28Type> = ({
  chatList,
  rectangle522,
  rectangle5221,
  group1949,
}) => {
  return (
    <div className="h-[844px] w-[375.9px] flex flex-col items-start justify-start gap-[26.200000000000045px] min-w-[375.8999999999997px] max-w-full text-left text-6xl text-darkslateblue-100 font-syne lg:flex-1 mq750:min-w-full">
      <div className="self-stretch flex flex-row items-start justify-start pt-[25.699999999999815px] px-24 pb-[29.800000000000185px] relative mq450:pl-5 mq450:pr-5 mq450:box-border">
        <h2 className="m-0 relative text-inherit font-bold font-inherit z-[1] mq450:text-xl">
          Kleenestar
        </h2>
        <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
          <img
            className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full"
            alt=""
            src="/rectangle-691.svg"
          />
          <img
            className="absolute top-[33px] left-[328.4px] w-[20.9px] h-[20.9px] z-[1]"
            loading="lazy"
            alt=""
            src="/pennewsquaresvgrepocom.svg"
          />
          <img
            className="absolute top-[16.1px] left-[25.8px] w-[52.1px] h-[54.8px] z-[1]"
            loading="lazy"
            alt=""
            src="/group-6721.svg"
          />
        </div>
      </div>
      <img
        className="self-stretch h-[580.1px] relative max-w-full overflow-hidden shrink-0 object-cover"
        loading="lazy"
        alt=""
        src={chatList}
      />
      <div className="self-stretch flex flex-col items-start justify-start pt-[15.199999999999818px] pb-[15.200000000000273px] pr-[25.699999999999815px] pl-[25.800000000000185px] relative text-mini font-montserrat">
        <img
          className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full"
          alt=""
          src="/rectangle-690.svg"
        />
        <button className="cursor-pointer [border:none] pt-[13.800000000000182px] px-[67.39999999999964px] pb-[14.499999999999543px] bg-[transparent] flex flex-row items-start justify-start relative mq450:pl-5 mq450:pr-5 mq450:box-border">
          <div className="relative text-mini font-medium font-montserrat text-darkslateblue-100 text-left z-[2]">
            Add team to workspace
          </div>
          <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
            <img
              className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[1]"
              alt=""
              src={rectangle522}
            />
            <img
              className="absolute top-[11px] left-[17.1px] w-[24.9px] h-[25.1px] z-[2]"
              alt=""
              src="/usersgrouproundedsvgrepocom.svg"
            />
          </div>
        </button>
        <div className="self-stretch flex flex-row items-start justify-start pt-[13.800000000000182px] px-[67.59999999999945px] pb-[14.499999999999543px] relative mq450:pl-5 mq450:pr-5 mq450:box-border">
          <div className="relative font-medium inline-block min-w-[118.3px] z-[3]">
            Craig Donovan
          </div>
          <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
            <img
              className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[2]"
              alt=""
              src={rectangle5221}
            />
            <img
              className="absolute top-[4.3px] left-[11.6px] w-[38.5px] h-[38.5px] z-[3]"
              loading="lazy"
              alt=""
              src="/group-2864.svg"
            />
            <img
              className="absolute top-[17.3px] left-[285.5px] w-[22px] h-[12.6px] z-[3]"
              loading="lazy"
              alt=""
              src={group1949}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default FrameComponent28;
