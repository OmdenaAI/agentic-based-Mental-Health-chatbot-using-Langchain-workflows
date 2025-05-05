import { Link } from "react-router-dom";
import hero_image from "./assets/green_life_happy_1.jpg";

const Hero = () => {
  return (
    <section
      className="relative w-full h-screen bg-cover bg-center bg-no-repeat"
      style={{
        backgroundImage: `url(${hero_image})`,
      }}
    >
      {/* Content */}
      <div className="relative z-10 flex flex-col justify-center items-end h-full text-right text-white pr-10">
        <span className="flex flex-col items-end gap-y-2 mb-4">
          <h1 className="text-[5rem] font-bold">
            Experience a <span className="text-green-300">GreenLife</span>
          </h1>
          <h1 className="text-3xl/14">
            - where your mental well-being comes first
          </h1>
        </span>

        <p className="text-xl mb-6 max-w-2xl">
          GreenLife is your personal mental wellness companion—always ready to
          listen, understand, and support you.
        </p>

        <div className="flex flex-col items-end gap-4 w-full max-w-md">
          <label htmlFor="feeling" className="text-white text-lg font-semibold">
            How are you feeling today?
          </label>
          <div className="relative w-full">
            <input
              id="feeling"
              type="text"
              placeholder="How are you feeling today?"
              className="w-full px-6 py-3 pr-36 bg-white text-green-400 text-lg font-semibold rounded-sm transition focus:outline-none focus:ring-2 focus:ring-green-300"
            />

            <Link to="/chat">
              <button
                type="submit"
                className="absolute top-1/2 right-2 -translate-y-1/2 px-4 py-2 bg-green-500 hover:bg-green-600 text-white text-sm font-semibold rounded-sm transition cursor-pointer"
              >
                Start Chatting
              </button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

// Experience a GreenLife — where your mental well-being comes first.
