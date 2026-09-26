import Header from "../components/Header"
import LeftSidebar from "../components/sidebar/LeftSidebar"
import RightSidebar from "../components/sidebar/RightSidebar"
import Sidebar from "../components/sidebar/Sidebar"

const Prompt = () => {
  return (
	<div className="flex">
		{/* <Header/> */}
		<LeftSidebar/>
		<div className="flex flex-2 items-end p-6">
			<textarea
				maxLength="2000"
				placeholder="Posez une question ..."
				id="message-input"
				name="message"
				autoComplete="off"
				rows="1"
				className="flex-1 border h-15 rounded-2xl bg-transparent resize-none outline-none text-sm placeholder-gray-500 py-2 px-5"
			></textarea>
		</div>
		<RightSidebar/>
	</div>
  )
}

export default Prompt
