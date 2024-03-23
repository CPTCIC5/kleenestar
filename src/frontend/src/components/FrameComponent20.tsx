import { FunctionComponent, useMemo, type CSSProperties } from "react";

export type FrameComponent20Type = {
  rectangle516?: string;
  pinterest?: string;
  pinterestIsAVisualDiscove?: string;
  forBrandsLookingToInspire?: string;
  products?: string;
  path28?: string;
  component660?: string;
  e91958eb97430e819064f3?: string;

  /** Style props */
  propWidth?: CSSProperties["width"];
  propAlignSelf?: CSSProperties["alignSelf"];
  propWidth1?: CSSProperties["width"];
  propWidth2?: CSSProperties["width"];
  propAlignSelf1?: CSSProperties["alignSelf"];
  propRight?: CSSProperties["right"];
  propMinWidth?: CSSProperties["minWidth"];
  propLeft?: CSSProperties["left"];
};

const FrameComponent20: FunctionComponent<FrameComponent20Type> = ({
  rectangle516,
  pinterest,
  pinterestIsAVisualDiscove,
  forBrandsLookingToInspire,
  products,
  path28,
  component660,
  e91958eb97430e819064f3,
  propWidth,
  propAlignSelf,
  propWidth1,
  propWidth2,
  propAlignSelf1,
  propRight,
  propMinWidth,
  propLeft,
}) => {
  const transformingStyle: CSSProperties = useMemo(() => {
    return {
      width: propWidth,
    };
  }, [propWidth]);

  const pinterestIsAStyle: CSSProperties = useMemo(() => {
    return {
      alignSelf: propAlignSelf,
      width: propWidth1,
    };
  }, [propAlignSelf, propWidth1]);

  const frameDiv5Style: CSSProperties = useMemo(() => {
    return {
      width: propWidth2,
      alignSelf: propAlignSelf1,
    };
  }, [propWidth2, propAlignSelf1]);

  const comingSoonStyle: CSSProperties = useMemo(() => {
    return {
      right: propRight,
    };
  }, [propRight]);

  const productsStyle: CSSProperties = useMemo(() => {
    return {
      minWidth: propMinWidth,
    };
  }, [propMinWidth]);

  const e91958eb97430e819064f3IconStyle: CSSProperties = useMemo(() => {
    return {
      left: propLeft,
    };
  }, [propLeft]);

  return (
    <div className="h-[282.2px] w-[407px] relative max-w-full text-left text-mini text-darkslateblue-100 font-montserrat">
      <img
        className="absolute top-[0px] left-[0px] w-[407.5px] h-[282px]"
        alt=""
        src={rectangle516}
      />
      <div className="absolute top-[0.2px] left-[0.1px] w-full flex flex-col items-start justify-start pt-[74.10000000000002px] px-[23.40000000000009px] pb-[35.799999999999955px] box-border gap-[16.600000000000023px] h-full">
        <div
          className="w-[336.9px] flex flex-col items-start justify-start gap-[7.5px] max-w-full"
          style={transformingStyle}
        >
          <div className="flex flex-row items-start justify-start pt-0 px-0 pb-[4.100000000000023px] text-lg">
            <div className="relative font-semibold inline-block min-w-[90.3px] z-[1]">
              {pinterest}
            </div>
          </div>
          <div className="self-stretch flex flex-col items-start justify-start gap-[7.499999999999886px]">
            <div
              className="self-stretch relative z-[1]"
              style={pinterestIsAStyle}
            >
              {pinterestIsAVisualDiscove}
            </div>
            <div
              className="w-[289.1px] flex flex-row items-start justify-start relative"
              style={frameDiv5Style}
            >
              <div className="flex-1 relative shrink-0 z-[1]">
                {forBrandsLookingToInspire}
              </div>
              <h1
                className="!m-[0] w-[231.7px] absolute top-[-15.7px] right-[-6.7px] text-11xl font-bold font-syne text-white inline-block shrink-0 z-[4] mq1000:text-5xl mq450:text-lg"
                style={comingSoonStyle}
              >
                Coming soon
              </h1>
            </div>
          </div>
          <div
            className="relative inline-block min-w-[75.5px] z-[1]"
            style={productsStyle}
          >
            {products}
          </div>
        </div>
        <div className="self-stretch h-[12.5px] flex flex-row items-start justify-start pt-0 px-0 pb-[10.399999999999975px] box-border max-w-full">
          <img
            className="h-[2.1px] flex-1 relative max-w-full overflow-hidden z-[1]"
            loading="lazy"
            alt=""
            src={path28}
          />
        </div>
        <button
  className="cursor-pointer relative"
  style={{
    backgroundColor: "#1C274C",
    color: "white",
    borderRadius: "50px",
    width: "50%", // Set width to 100% for responsiveness
    height: "40px",
    flexShrink: 0,
    // marginBottom:'1000px',
    border: "none", // If you want to remove the border
    padding: 0, // If you want to remove padding
    alignSelf: "stretch", // If you want the button to stretch vertically
    position: "relative", // If you want to position child elements relatively
    maxWidth: "454px", // Set maximum width for larger screens
  }}
>
  <span style={{ marginRight: '10px' ,color: '#FFF',
fontFamily: 'Montserrat',
fontSize: '15px',
fontStyle: 'normal',
fontWeight: '500',
lineHeight: 'normal',}}>Connect</span>
  <img
    className="absolute top-[50%] transform -translate-y-1/2 right-2 w-[21.7px] h-[18.5px] z-[2]"
    alt=""
    src="/group-2051.svg"
  />
</button>
        <div className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
          <img
            className="absolute top-[223.9px] left-[331.6px] w-[51px] h-[27.6px] z-[1]"
            loading="lazy"
            alt=""
            src={component660}
          />
          {/* <img
            className="absolute top-[216.5px] left-[23.4px] w-[145px] h-[42.5px] z-[1]"
            alt=""
            src="/rectangle-512-4.svg"
          />
          <img
            className="absolute top-[228px] left-[125.4px] w-[21.7px] h-[18.5px] z-[2]"
            loading="lazy"
            alt=""
            src="/group-2051.svg"
          /> */}
          <img
            className="absolute top-[24.5px] left-[25.5px] w-[40.4px] h-[40.4px] object-cover z-[1]"
            loading="lazy"
            alt=""
            src={e91958eb97430e819064f3}
            style={e91958eb97430e819064f3IconStyle}
          />
          <img
            className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[3]"
            alt=""
            src="/rectangle-700.svg"
          />
        </div>
      </div>
    </div>
  );
};

export default FrameComponent20;
