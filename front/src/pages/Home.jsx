import Header from "../components/Header"
import Notebooks from "../components/Notebooks"

export const Home = () => {
  return (
	<div>
		<Header/>
		<div className="flex justify-center">
		<div className="max-w-6xl w-full py-4">
			<Notebooks/>
		</div>
      </div></div>
  )
}

