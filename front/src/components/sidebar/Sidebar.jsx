
const Sidebar = ({children}) => {
  return (
	<div className="h-screen flex-1 p-10">
		<div className=" h-full bg-gray-100/3 shadow-sm rounded-2xl p-10">{children}</div>
	</div>
  )
}

export default Sidebar
