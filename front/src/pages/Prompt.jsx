import Header from "../components/Header"
import Sidebar from "../components/Sidebar"

const Prompt = () => {
  return (
	<div>
		<Header/>
		<div className="flex p-4">
			<Sidebar/>
			<div className="flex-2"></div>
			<Sidebar/>
		</div>
	</div>
  )
}

export default Prompt
